class WagtailMathJaxController extends window.StimulusModule.Controller {
    connect() {
        initMathJaxPreview(this.element.id);
    }
}

window.wagtail.app.register('wagtailmathjax', WagtailMathJaxController);
