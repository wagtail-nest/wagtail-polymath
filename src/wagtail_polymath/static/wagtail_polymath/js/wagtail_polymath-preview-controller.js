class PolymathPreviewController extends window.StimulusModule.Controller {
    connect() {
        initPolymathTextareaPreview(this.element.id);
    }
}

window.wagtail.app.register('polymath-textarea-controller', PolymathPreviewController);
