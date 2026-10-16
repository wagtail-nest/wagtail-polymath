let resolveMathJaxReady;
const mathJaxReady = new Promise((resolve) => {
  resolveMathJaxReady = resolve;
});

// Extra config from WAGTAIL_POLYMATH["mathjax_config"], passed on this script tag
const polymathUserConfig = JSON.parse((document.currentScript && document.currentScript.dataset.polymathConfig) || "{}");

// Objects merge; arrays and other values replace
function polymathMergeConfig(target, source) {
  const isObject = (value) => value !== null && typeof value === "object" && !Array.isArray(value);
  for (const [key, value] of Object.entries(source)) {
    target[key] = isObject(value) && isObject(target[key]) ? polymathMergeConfig(target[key], value) : value;
  }
  return target;
}

if (window.MathJax && window.MathJax.version) {
  // MathJax was loaded before this script: don't clobber it, just wait for startup.
  if (Object.keys(polymathUserConfig).length) {
    console.warn("wagtail-polymath: MathJax was already loaded, so WAGTAIL_POLYMATH['mathjax_config'] was not applied.");
  }
  window.MathJax.startup.promise.then(resolveMathJaxReady);
} else {
  window.MathJax = polymathMergeConfig(
    { loader: { load: ["input/asciimath"] } },  // "AM" isn't in tex-mml-chtml; add it explicitly
    polymathUserConfig,
  );
  // Set after merging, so user config can't replace the hook the preview relies on
  window.MathJax.startup = {
    ...window.MathJax.startup,
    ready() {
      // @see https://docs.mathjax.org/en/latest/web/actions.html
      MathJax.startup.defaultReady();
      MathJax.startup.promise.then(resolveMathJaxReady);
    },
  };
}


class Preview {
  constructor(previewId, bufferId, inputId) {
    this.preview = document.getElementById(previewId);
    this.buffer = document.getElementById(bufferId);
    this.input = document.getElementById(inputId);
    this.delay = 150;        // delay after keystroke before updating
    this.timeout = null;     // the setTimeout id
    this.mjRunning = false;  // true while waiting for / running MathJax
    this.mjPending = false;  // true if input changed during a typeset
    this.oldText = null;     // last text sent to MathJax
  }

  // Swap buffer/preview so the freshly typeset one is shown.
  swapBuffers() {
    const buffer = this.preview;
    const preview = this.buffer;
    this.buffer = buffer;
    this.preview = preview;
    buffer.style.visibility = "hidden";
    buffer.style.position = "absolute";
    preview.style.position = "";
    preview.style.visibility = "";
  }

  // Debounce: typeset only after a pause in typing.
  update() {
    clearTimeout(this.timeout);
    this.timeout = setTimeout(() => this.createPreview(), this.delay);
  }

  createPreview() {
    this.timeout = null;

    // A typeset (or the wait for MathJax) is in flight: rerun when it finishes.
    if (this.mjRunning) {
      this.mjPending = true;
      return;
    }

    const text = this.input.value;
    if (text === this.oldText) return;
    this.oldText = text;

    this.mjRunning = true;
    this.mjPending = false;

    const buffer = this.buffer;  // capture: swapBuffers may run before the promise settles

    mathJaxReady
      .then(() => {
        MathJax.typesetClear([buffer]);  // drop metadata from the previous render
        buffer.innerHTML = text;
        return MathJax.typesetPromise([buffer]);
      })
      .then(() => this.swapBuffers())
      .catch((err) => {
        this.oldText = null;  // allow a retry on the next change
        console.error("MathJax typeset failed:", err);
      })
      .finally(() => {
        this.mjRunning = false;
        if (this.mjPending) {
          this.mjPending = false;
          this.update();
        }
      });
  }
}

function initPolymathTextareaPreview(id) {
  const target = document.getElementById(id);
  if (!target) {
    return;
  }

  const preview = new Preview(
    "PolymathTextareaPreview-" + id,
    "PolymathTextareaBuffer-" + id,
    id
  );

  window.wagtailPolymathPreviews = window.wagtailPolymathPreviews || {};
  window.wagtailPolymathPreviews[id] = preview;

  if (target.value) {
    preview.update();
  }

  target.addEventListener("input", () => preview.update());
}
