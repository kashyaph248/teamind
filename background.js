const API_URL = "http://127.0.0.1:8000/api/summarize-text";

// Create right-click menu
chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: "teammind-summarize",
    title: "Summarize with TeamMind AI",
    contexts: ["selection"]
  });
});

// Handle right-click click
chrome.contextMenus.onClicked.addListener((info, tab) => {
  if (info.menuItemId !== "teammind-summarize" || !tab || tab.id == null) return;

  chrome.scripting.executeScript({
    target: { tabId: tab.id },
    func: async (apiUrl) => {
      const selected = window.getSelection().toString().trim();
      if (!selected) {
        alert("TeamMind AI: No text selected.");
        return;
      }

      try {
        const res = await fetch(apiUrl, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ text: selected })
        });

        if (!res.ok) {
          let msg = "Request failed.";
          try {
            const data = await res.json();
            if (data.detail) msg = data.detail;
          } catch (e) {}
          alert("TeamMind AI Error: " + msg);
          return;
        }

        const data = await res.json();
        const summary = data.summary || "No summary returned.";
        alert("TeamMind AI Summary:\n\n" + summary);
      } catch (err) {
        alert("TeamMind AI Error: " + (err.message || "Something went wrong."));
      }
    },
    args: [API_URL]
  });
});

