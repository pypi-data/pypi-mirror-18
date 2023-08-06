{% extends "base.tpl" %}

{% block content %}
  <div class="page-header">
    <h1>ardj dashboard</h1>
  </div>

  <div id="player" class="player" data-stream="http://127.0.0.1:8000/live.mp3">
  </div>

  <ul class="nav nav-tabs hometabs">
    <li class="active"><a href="#queue">Queue</a></li>
    <li><a href="#recent">Recent</a></li>
  </ul>

  <div id="queue_tab" class="tab">
    {% if queue %}
      <table class="table tracklist">
        <thead>
          <tr>
            <th class="num">#</th>
            <th class="wide">Track title</th>
            <th title="Play count" class="num">Cnt</th>
            <th title="Track weight" class="num">Wgt</th>
            <th class="dur">Dur</th>
          </tr>
        </thead>
        <tbody>
          {% for track in queue %}
            <tr>
              <td class="num">{{ track.id }}</td>
              <td>
                {% if track.artist and track.title %}
                  <a href="/artists/{{ track.artist }}">{{ track.artist }}</a> &mdash; <a href="/track/{{ track.id }}">{{ track.title }}</a>
                {% else %}
                  <a href="/tracks/{{ track.id }}">{{ track.filename }}</a>
                {% endif %}
                <div class="actions">
                  <a class="btn btn-default btn-xs async" href="/track/{{ track.id }}/rocks" title="Track rocks, play more often"><i class="glyphicon glyphicon-ok"></i></a>
                  <a class="btn btn-default btn-xs async" href="/track/{{ track.id }}/sucks" title="Track sucks, play less often"><i class="glyphicon glyphicon-remove"></i></a>
                  <a class="btn btn-default btn-xs async" href="/track/{{ track.id }}/queue" title="Add to playback queue"><i class="glyphicon glyphicon-time"></i></a>
                  <a class="btn btn-default btn-xs" href="/track/{{ track.id }}/download" title="Download track"><i class="glyphicon glyphicon-download"></i></a>
                  {% for l in track.labels %}
                    <a class="btn btn-default btn-xs" href="/tags/{{ l }}" title="Show more track with this label"><i class="glyphicon glyphicon-tag"></i> {{ l }}</a>
                  {% endfor %}
                </div>
              </td>
              <td class="num">{% if track.count %}{{ track.count }}{% else %}—{% endif %}</td>
              <td class="num">{% if track.weight %}{{ track.weight }}{% else %}—{% endif %}</td>
              <td class="dur">{{ track.duration }}</td>
            </tr>
          {% endfor %}
        </tbody>
      </table>
    {% else %}
      <p>Empty.  Click the buttons to queue some tracks.</p>
    {% endif %}
  </div>

  <div id="recent_tab" class="tab" style="display:none">
    {% if tracks %}
      <table class="table tracklist">
        <thead>
          <tr>
            <th class="num">#</th>
            <th class="wide">Track title</th>
            <th title="Play count" class="num">Cnt</th>
            <th title="Track weight" class="num">Wgt</th>
            <th class="dur">Dur</th>
          </tr>
        </thead>
        <tbody>
          {% for track in tracks %}
            <tr>
              <td class="num">{{ track.id }}</td>
              <td>
                {% if track.artist and track.title %}
                  <a href="/artists/{{ track.artist }}">{{ track.artist }}</a> &mdash; <a href="/track/{{ track.id }}">{{ track.title }}</a>
                {% else %}
                  <a href="/tracks/{{ track.id }}">{{ track.filename }}</a>
                {% endif %}
                <div class="actions">
                  <a class="btn btn-default btn-xs async" href="/track/{{ track.id }}/rocks" title="Track rocks, play more often"><i class="glyphicon glyphicon-ok"></i></a>
                  <a class="btn btn-default btn-xs async" href="/track/{{ track.id }}/sucks" title="Track sucks, play less often"><i class="glyphicon glyphicon-remove"></i></a>
                  <a class="btn btn-default btn-xs async" href="/track/{{ track.id }}/queue" title="Add to playback queue"><i class="glyphicon glyphicon-time"></i></a>
                  <a class="btn btn-default btn-xs" href="/track/{{ track.id }}/download" title="Download track"><i class="glyphicon glyphicon-download"></i></a>
                  {% for l in track.labels %}
                    <a class="btn btn-default btn-xs" href="/tags/{{ l }}" title="Show more track with this label"><i class="glyphicon glyphicon-tag"></i> {{ l }}</a>
                  {% endfor %}
                </div>
              </td>
              <td class="num">{% if track.count %}{{ track.count }}{% else %}—{% endif %}</td>
              <td class="num">{% if track.weight %}{{ track.weight }}{% else %}—{% endif %}</td>
              <td class="dur">{{ track.duration }}</td>
            </tr>
          {% endfor %}
        </tbody>
      </table>
    {% else %}
      <p>Hmm, nothing was played.</p>
      <p>Looks like your radio is not fully set up.  Please <a href="/upload">upload some music</a>.</p>
    {% endif %}
  </div>

{% endblock %}
