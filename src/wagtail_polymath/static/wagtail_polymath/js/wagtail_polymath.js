class Preview {
  constructor(previewId, bufferId, inputId) {
    this.preview = document.getElementById(previewId);
    this.buffer = document.getElementById(bufferId);
    this.input = document.getElementById(inputId);
    this.delay = 150;        // delay after keystroke before updating
    this.timeout = null;     // store setTimeout id
    this.mjRunning = false;  // true when MathJax is processing
    this.mjPending = false;  // true when a typeset has been queued
    this.oldText = null;     // used to check if an update is needed
  }

  // Swap buffer/preview so the freshly typeset one is shown.
  swapBuffers() {
    let buffer = this.preview, preview = this.buffer;
    this.buffer = buffer;
    this.preview = preview;
    buffer.style.visibility = "hidden";
    buffer.style.position = "absolute";
    preview.style.position = "";
    preview.style.visibility = "";
  }

  // Debounce: typeset only after a pause in typing.
  update() {
    if (this.timeout) {
      clearTimeout(this.timeout);
    }

    this.timeout = setTimeout(() => this.createPreview(), this.delay);
  }

  // Render input into the hidden buffer, then typeset it.
  createPreview() {
    this.timeout = null;
    this.mjRunning = true;
    this.mjPending = false;

    const text = this.input.value;
    if (text === this.oldText) return;
    this.oldText = text;

    let buffer = this.buffer;  // capture: SwapBuffers may run before the promise settles


    MathJax.typesetClear([buffer]);  // drop metadata from the previous render

    buffer.innerHTML = text;

    MathJax.typesetPromise([buffer])
      .then(() => {
        this.mjRunning = false;
        if (this.mjPending) {
          this.update();
        }
        else {
          this.previewDone();
        }
      })
      .catch((err) => console.error("MathJax typeset failed:", err));
  }

  previewDone() {
    this.mjRunning = this.mjPending = false;
    this.swapBuffers();
  }
}


function initMathJaxPreview(id) {
  const target = document.getElementById(id);
  if (!target) {
    return;
  }

  const preview = new Preview("MathPreview-" + id, "MathBuffer-" + id, id);

  window.wagtailMathPreviews = window.wagtailMathPreviews || {};
  window.wagtailMathPreviews[id] = preview;

  if (target.value) {
    preview.update();
  }

  target.addEventListener("keyup",  () => {
    if (this.mjRunning) {
      this.mjPending = true;
    }
    else {
      preview.update()
    }
  });
}

window.MathJax = {
  loader: { load: ["input/asciimath"] },  // "AM" isn't in tex-mml-chtml; add it explicitly
  tex: {
    inlineMath: { '[+]': [['$', '$']] }
  },
};
