const submitButton = document.getElementById("submit");
const sentenceInput = document.getElementById("sentence");
const preprocessedOutput = document.getElementById("preprocessed");
const tokensOutput = document.getElementById("tokens");
const syntaxOutput = document.getElementById("syntax");
const semanticOutput = document.getElementById("semantic");
const intentOutput = document.getElementById("intent");
const irOutput = document.getElementById("ir");
const codeOutput = document.getElementById("code");
const copyCodeButton = document.getElementById("copy-code");
const copyStatus = document.getElementById("copy-status");
const tabButtons = document.querySelectorAll(".tab-button");
const tabPanels = document.querySelectorAll(".tab-panel");

const API_URL = "/process";

const render = (element, data) => {
  element.textContent = JSON.stringify(data, null, 2);
};

const renderTokens = (tokens) => {
  if (!tokens || tokens.length === 0) {
    tokensOutput.textContent = "[]";
    return;
  }
  tokensOutput.textContent = tokens
    .map((token) => `${token.value} : ${token.type}`)
    .join("\n");
};

const setActiveTab = (tabName) => {
  tabButtons.forEach((button) => {
    button.classList.toggle("is-active", button.dataset.tab === tabName);
    button.setAttribute("aria-selected", button.dataset.tab === tabName ? "true" : "false");
  });
  tabPanels.forEach((panel) => {
    panel.classList.toggle("is-active", panel.dataset.panel === tabName);
    panel.hidden = panel.dataset.panel !== tabName;
  });
};

tabButtons.forEach((button) => {
  button.addEventListener("click", () => {
    setActiveTab(button.dataset.tab);
  });
});

const selectCodeBlock = () => {
  const selection = window.getSelection();
  const range = document.createRange();
  range.selectNodeContents(codeOutput);
  selection.removeAllRanges();
  selection.addRange(range);
};

const copyViaTextarea = (text) => {
  const tempInput = document.createElement("textarea");
  tempInput.value = text;
  tempInput.setAttribute("readonly", "");
  tempInput.style.position = "fixed";
  tempInput.style.opacity = "0";
  tempInput.style.pointerEvents = "none";
  tempInput.style.top = "0";
  tempInput.style.left = "0";
  document.body.appendChild(tempInput);
  tempInput.focus();
  tempInput.select();
  tempInput.setSelectionRange(0, tempInput.value.length);

  let copied = false;
  try {
    copied = document.execCommand("copy");
  } catch (error) {
    copied = false;
  }

  document.body.removeChild(tempInput);
  return copied;
};

const copyGeneratedCode = async (text) => {
  if (navigator.clipboard) {
    try {
      await navigator.clipboard.writeText(text);
      return true;
    } catch (error) {
      return copyViaTextarea(text);
    }
  }
  return copyViaTextarea(text);
};

copyCodeButton.addEventListener("click", async () => {
  const codeText = codeOutput.textContent.trim();
  if (!codeText) {
    copyStatus.textContent = "No code to copy.";
    return;
  }

  try {
    const copied = await copyGeneratedCode(codeText);

    if (!copied) {
      selectCodeBlock();
      copyStatus.textContent = "Clipboard blocked. Press Ctrl+C to copy selected code.";
      return;
    }

    copyStatus.textContent = "Copied.";
  } catch (error) {
    selectCodeBlock();
    copyStatus.textContent = "Clipboard blocked. Press Ctrl+C to copy selected code.";
  }
});

submitButton.addEventListener("click", async () => {
  const sentence = sentenceInput.value.trim();
  if (!sentence) {
    preprocessedOutput.textContent = "\"\"";
    renderTokens([]);
    render(syntaxOutput, { valid: false, message: "Please enter a sentence." });
    render(semanticOutput, {});
    render(intentOutput, {});
    render(irOutput, {});
    codeOutput.textContent = "";
    copyStatus.textContent = "";
    return;
  }

  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ sentence }),
    });

    if (!response.ok) {
      throw new Error(`Server error: ${response.status}`);
    }

    const data = await response.json();
    preprocessedOutput.textContent = JSON.stringify(data.preprocessed ?? "", null, 2);
    renderTokens(data.tokens);
    render(syntaxOutput, data.syntax_status);
    render(semanticOutput, data.semantic_status);
    render(intentOutput, { intent: data.intent, entities: data.entities });
    render(irOutput, data.ir);
    codeOutput.textContent = data.code || "";
    copyStatus.textContent = "";
  } catch (error) {
    render(syntaxOutput, { valid: false, message: error.message });
    render(semanticOutput, {});
    render(intentOutput, {});
    render(irOutput, {});
    codeOutput.textContent = "";
    copyStatus.textContent = "";
  }
});
