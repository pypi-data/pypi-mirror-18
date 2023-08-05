define([
  'base/js/namespace'
], function(Jupyter) {
  function load_ipython_extension() {
    console.log("~~ nbextension (frontend) loaded");
  };
  return {
    load_ipython_extension: load_ipython_extension
  };
});
