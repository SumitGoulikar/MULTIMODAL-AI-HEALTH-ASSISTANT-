(function () {
  const THEME_KEY = "theme";
  const root = document.documentElement;
  const btn = document.getElementById("themeToggle");
  const label = document.getElementById("themeToggleLabel");

  function getPreferredTheme() {
    const stored = window.localStorage.getItem(THEME_KEY);
    if (stored === "light" || stored === "dark") return stored;
    return window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches
      ? "dark"
      : "light";
  }

  function setTheme(theme) {
    const isDark = theme === "dark";
    root.classList.toggle("dark", isDark);
    // Button label indicates the next mode.
    if (label) label.textContent = isDark ? "Switch to Light" : "Switch to Dark";
  }

  function init() {
    if (!btn) return;
    const theme = getPreferredTheme();
    setTheme(theme);

    btn.addEventListener("click", function () {
      const next = root.classList.contains("dark") ? "light" : "dark";
      window.localStorage.setItem(THEME_KEY, next);
      setTheme(next);
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();

