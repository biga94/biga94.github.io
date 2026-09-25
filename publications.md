---
layout: page
title: Publications
permalink: /publications/
---

{%- assign pubs = site.data.publications -%}
{%- if pubs and pubs.size > 0 -%}
{%- assign pubs = pubs | sort: "year" | reverse -%}
<ul class="publication-list">
  {%- for pub in pubs %}
  <li>
    {%- if pub.url %}<a href="{{ pub.url }}" target="_blank" rel="noopener">{{ pub.title }}</a>{%- else %}{{ pub.title }}{%- endif -%}
    {%- if pub.journal %}. <em>{{ pub.journal }}</em>{%- endif -%}
    {%- if pub.year and pub.year != 0 %} ({{ pub.year }}){%- endif -%}
  </li>
  {%- endfor %}
</ul>
{%- else -%}
<p>Publication list loading — check back shortly.</p>
{%- endif -%}

{%- include person-schema.html -%}
