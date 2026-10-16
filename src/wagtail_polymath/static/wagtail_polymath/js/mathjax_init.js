(function () {
  // Extra config from WAGTAIL_POLYMATH["mathjax_config"], passed on this script tag
  const script = document.currentScript;
  const userConfig = JSON.parse((script && script.dataset.polymathConfig) || "{}");

  // Objects merge; arrays and other values replace
  const isObject = (value) => value !== null && typeof value === "object" && !Array.isArray(value);
  const merge = (target, source) => {
    for (const [key, value] of Object.entries(source)) {
      target[key] = isObject(value) && isObject(target[key]) ? merge(target[key], value) : value;
    }
    return target;
  };

  window.MathJax = merge({ loader: { load: ["input/asciimath"] } }, userConfig);
})();
