const submitButton = document.getElementById("submit");
const sentenceInput = document.getElementById("sentence");
const preprocessedOutput = document.getElementById("preprocessed");
const tokensOutput = document.getElementById("tokens");
const syntaxOutput = document.getElementById("syntax");
const semanticOutput = document.getElementById("semantic");
const intentOutput = document.getElementById("intent");
const irOutput = document.getElementById("ir");
const codeOutput = document.getElementById("code");
const tabButtons = document.querySelectorAll(".tab-button");
const tabPanels = document.querySelectorAll(".tab-panel");

const API_URL = "http://127.0.0.1:8000/process";

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
  } catch (error) {
    render(syntaxOutput, { valid: false, message: error.message });
    render(semanticOutput, {});
    render(intentOutput, {});
    render(irOutput, {});
    codeOutput.textContent = "";
  }
});
