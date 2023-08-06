coop HTML Editor
===============================================

* `What is coop_html_editor good for?`_
* `Quick start`_
* `Options`_

.. _What is coop_html_editor good for?: #good-for
.. _Quick start?: #quick-start
.. _Options?: #options

.. _good-for:

What is coop_html_editor good for?
------------------------------------
coop_html_editor is a backend for using inline HTML editor into a Django site.
It enables inline editing for your HTML content.
It includes a django Form and a Widget helper.
It supports Aloha Editor and CK Editor

.. _quick-start:

Quick start
------------------------------------
In settings.py, add 'coop_html_editor' to the INSTALLED_APPS
In urls.py add ``(r'^html-editor/', include('coop_html_editor.urls'))`` to your urlpatterns

Then create a form. For example something like ::

    import floppyforms
    from models import Note
    from coop_html_editor.widgets import InlineHtmlInput
    
    class NoteForm(floppyforms.ModelForm):
        class Meta:
            model = Note
            fields = ('text',)
            widgets = {
                'text': InlineHtmlInput(),
            }


Let's assume that you've a ``form`` variable pointing on an instance of a NoteForm.
In the template file, call the form and don't forget to put ``{{form.media}}`` in the headers.

.. _options:

Options
------------------------------------

InlineHtmlInput has a "provider" that allows you to add local links to your models (articles, contacts, whatever) easily, through an autocomplete field that will search for objects based on rules you defined for each model :

* search this kind of models using get_absolute_url()
* search this kind of models using another method
* search this kind of models using a specified model field

You can set the ``HTML_EDITOR_LINK_MODELS`` setting in your settings.py to tell which django models will be available in the auto-complete field of the "add link" widget like this ::

    HTML_EDITOR_LINK_MODELS = ('coop_local.Article', 'calendar.Event', )
    
    
djaloha requires jquery and is provided by default with jquery.1.7.2. You can change the jquery version if needed ::

    HTML_EDITOR_JQUERY = 'js/jquery.1.7.2.js'
    
    
Aloha has a nice plugin architecture. coop_html_editor includes by default the main Aloha plugins. You may want to have a different set of plugins.
Please refer to the Aloha docs for more information on plugins ::

    ALOHA_PLUGINS = (
        "common/format",
        "common/highlighteditables",
        "common/list",
        "common/link",
        "common/undo",
        "common/paste",
        "common/commands",
        "common/image",
        "common/align",
        "extra/attributes",
        "common/characterpicker",
        "common/abbr",
        "common/horizontalruler",
        "common/table",
        "extra/browser",
    )
    

Please note that the ``ALOHA_PLUGINS`` setting is a global setting. If you need to change the set of plugins for a specific form field, you
can pass a similar tuple in the ``aloha_plugins`` attribute of your ``coop_html_editor`` widget.
The ``extra_aloha_plugins`` attribute will add additional plugins to the default set.

``HTML_EDITOR_INIT_URL`` setting make possible to overloaf the aloha init file of djaloha.
``html_editor_init_url`` attribute of ``InlineHtmlInput`` can also be used to overload it for a specific form field.

License
=======

coop_html_editor is based on apidev-djaloha is a fork from credis/djaloha (see http://github.com/credis/djaloha)

coop_html_editor uses the BSD license. see license.txt

Djaloha development was funded by `CREDIS <http://credis.org/>`_, FSE (European Social Fund) and Conseil Regional d'Auvergne.
