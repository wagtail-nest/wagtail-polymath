class Preview {
  constructor (previewId, bufferId, inputId) {
    this.preview = document.getElementById(previewId);
    this.buffer = document.getElementById(bufferId);
    this.input = document.getElementById(inputId);
    this.delay = 150;        // delay after keystroke before updating
    this.timeout = null;     // store setTimout id

    this.input.addEventListener("input", () => {
      if (this.timeout) {
        clearTimeout(this.timeout);
      }
      this.timeout = setTimeout(() => { this.render() }, this.delay);
    });

    document.addEventListener("DOMContentLoaded", () => { this.render() });
  }

  render () {
    if (this.preview.innerHTML === this.input.value) { return }

    this.preview.innerHTML = this.input.value;
    renderMathInElement(
      this.preview,
      {
        delimiters: [
          {left: '$$', right: '$$', display: true},
          {left: '$', right: '$', display: false},
          {left: '\\(', right: '\\)', display: false},
          {left: '\\[', right: '\\]', display: true}
        ],
        throwOnError : false
      }
    );
  }
}
