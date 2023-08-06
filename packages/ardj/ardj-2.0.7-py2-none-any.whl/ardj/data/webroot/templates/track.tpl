{% extends "base.tpl" %}

{% block content %}
  <div class="page-header">
    <h1>Track properties</h1>
  </div>

  <form method="post" class="form async">
    <div class="form-group">
      <label>Title:</label>
      <input type="text" class="form-control" name="title" value="{{ track.title }}" />
    </div>

    <div class="form-group">
      <label>Artist:</label>
      <input type="text" class="form-control" name="artist" value="{{ track.artist }}" />
    </div>

    <div class="form-group">
      <label>Labels:</label>
      <input type="text" class="form-control" name="labels" value="{{ track.labels }}" />
    </div>

    <div class="form-group">
      <button class="btn btn-primary">Save changes</button>
    </div>
  </form>
{% endblock %}
