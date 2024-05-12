// Update the preview area on input. Lifted directly from mathjax website examples
class Preview {
  //
  //  Get the preview and buffer DIV's
  //
  constructor (previewId, bufferId, inputId) {
    this.preview = document.getElementById(previewId);
    this.buffer = document.getElementById(bufferId);
    this.input = document.getElementById(inputId);
    this.delay = 150;        // delay after keystroke before updating
    this.timeout = null;     // store setTimout id
    this.mjRunning = false;  // true when MathJax is processing
    this.mjPending = false;  // true when a typeset has been queued
    this.oldText = null;     // used to check if an update is needed

    this.callback = MathJax.Callback(["CreatePreview", this]);
    this.callback.autoReset = true;  // make sure it can run more than once

    this.input.addEventListener("input", () => {
      if (this.timeout) {
        clearTimeout(this.timeout);
      }
      this.timeout = setTimeout(this.callback, this.delay);
    });

    document.addEventListener("DOMContentLoaded", () => { this.callback() });
  }

  //
  //  Switch the buffer and preview, and display the right one.
  //  (We use visibility:hidden rather than display:none since
  //  the results of running MathJax are more accurate that way.)
  //
  SwapBuffers () {
    var buffer = this.preview, preview = this.buffer;
    this.buffer = buffer; this.preview = preview;
    buffer.style.visibility = "hidden"; buffer.style.position = "absolute";
    preview.style.position = ""; preview.style.visibility = "";
  }

  //
  //  Creates the preview and runs MathJax on it.
  //  If MathJax is already trying to render the code, return
  //  If the text hasn't changed, return
  //  Otherwise, indicate that MathJax is running, and start the
  //    typesetting.  After it is done, call PreviewDone.
  //
  CreatePreview () {
    this.timeout = null;
    if (this.mjPending) return;
    var text = this.input.value;
    if (text === this.oldtext) return;
    if (this.mjRunning) {
      this.mjPending = true;
      MathJax.Hub.Queue(["CreatePreview", this]);
    }
    else {
      this.buffer.innerHTML = this.oldtext = text;
      this.mjRunning = true;
      MathJax.Hub.Queue(
	      ["Typeset", MathJax.Hub, this.buffer],
	      ["PreviewDone", this]
      );
    }
  }

  //
  //  Indicate that MathJax is no longer running,
  //  and swap the buffers to show the results.
  //
  PreviewDone () {
    this.mjRunning = this.mjPending = false;
    this.SwapBuffers();
  }
}
