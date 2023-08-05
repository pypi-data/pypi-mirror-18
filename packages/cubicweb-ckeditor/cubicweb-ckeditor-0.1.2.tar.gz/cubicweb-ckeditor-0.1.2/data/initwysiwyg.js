function buildWysiwygEditors(parent) {
    jQuery('textarea').each(function() {
        var cw_type = this.getAttribute('cubicweb:type');
        if (cw_type === 'fckeditor' || cw_type === 'wysiwyg') {
            // mark editor as instanciated, we may be called a number of times
            // (see _postAjaxLoad)
            this.setAttribute('cubicweb:type', 'ckeditor');
            if (typeof CKEDITOR != "undefined") {
                var fck = CKEDITOR.replace(this.id, {
                    customConfig: ckconfigpath,
                    defaultLanguage: cklang
                });
            } else {
                cw.log('fckeditor could not be found.');
            }
        }
    });
}


cw.utils.formContents = function formContents(elem) {
    var $elem, array, names, values;
    $elem = cw.jqNode(elem);
    array = $elem.serializeArray();

    if (typeof CKEDITOR !== 'undefined') {
        $elem.find('textarea').each(function (idx, textarea) {
            var ck = CKEDITOR.instances[textarea.id];
            if (ck) {
                array = jQuery.map(array, function (dict) {
                    if (dict.name === textarea.name) {
                        // filter out the textarea's - likely empty - value ...
                        return null;
                    }
                    return dict;
                });
                // ... so we can put the HTML coming from FCKeditor instead.
                array.push({
                    name: textarea.name,
                    value: ck.getData()
                });
            }
        });
    }

    names = [];
    values = [];
    jQuery.each(array, function (idx, dict) {
        names.push(dict.name);
        values.push(dict.value);
    });
    return [names, values];
};
