cat << 'EOF' > popup.js
const input = document.getElementById("input");
const btn = document.getElementById("summarizeBtn");
const output = document.getElementById("output");

btn.addEventListener("click", async () => {
  const text = input.value.trim();
  if (!text) {
    output.textContent = "Please paste some text.";
    return;
  }

  btn.disabled = true;
  btn.textContent = "Summarizing...";
  output.textContent = "";

  try {
    const res = await fetch("http://127.0.0.1:8000/api/summarize-text", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text })
    });

    if (!res.ok) {
      let msg = "Request failed.";
      try {
        const data = await res.json();
        if (data.detail) msg = data.detail;
      } catch (e) {}
      output.textContent = "Error: " + msg;
      return;
    }

    const data = await res.json();
    output.textContent = data.summary || "No summary returned.";
  } catch (err) {
    output.textContent = "Error: " + (err.message || "Something went wrong.");
  } finally {
    btn.disabled = false;
    btn.textContent = "Summarize";
  }
});
EOF

