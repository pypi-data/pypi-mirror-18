tinymce.init({
    selector: 'textarea',
    height: 250,
    plugins: 'searchreplace textcolor colorpicker table link anchor image imagetools media charmap hr code visualblocks',
    menubar: '',
    toolbar1: 'undo redo | searchreplace | bold italic underline strikethrough | forecolor backcolor | subscript superscript | outdent indent | alignleft aligncenter alignright alignjustify | bullist numlist | blockquote',
    toolbar2: 'formatselect fontsizeselect | table | link unlink | anchor | image media | charmap hr | visualblocks code',
    fontsize_formats: '0.5rem 0.75rem 1rem 1.15rem 1.25rem 1.5rem 1.75rem 2rem 2.5rem 3rem 4rem 5rem',
    paste_data_images: true,
    content_css : '/static/admin/tinymce/css/styles.css'
  });
