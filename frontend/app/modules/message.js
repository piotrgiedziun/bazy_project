// Message module
define([
  // Application.
  "app"
],

// Map dependencies from above array.
function(app) {

  // Create a new module.
  var Message = app.module();

  // Default Model.
  Message.Model = Backbone.Model.extend({
  
  });

  // Default Collection.
  Message.Collection = Backbone.Collection.extend({
    model: Message.Model
  });

  // Default View.
  Message.Views.Layout = Backbone.Layout.extend({
    template: "message"
  });

  // Return the module for AMD compliance.
  return Message;

});
