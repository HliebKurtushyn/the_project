(function(){
  'use strict';
  var populated = false;

  function renderCategoriesList(rawStr){
    var categories = [];
    if (!rawStr) return categories;
    try{
      categories = JSON.parse(rawStr);
      if (!Array.isArray(categories)) categories = [];
    }catch(e){
      console.error('Failed to parse categories JSON', e, rawStr);
      categories = [];
    }
    return categories;
  }

  function buildList(categories){
    var container = document.getElementById('categories-list');
    if (!container) return;
    container.innerHTML = '';
    if (!categories || categories.length === 0) {
      container.innerHTML = '<p class="text-muted">Категорій немає</p>';
      return;
    }
    categories.forEach(function(cat){
      var a = document.createElement('a');
      a.className = 'list-group-item list-group-item-action d-flex justify-content-between align-items-center';
      a.href = cat.url || '#';
      a.textContent = cat.name || cat.title || '—';

      if (cat.count != null) {
        var span = document.createElement('span');
        span.className = 'badge bg-secondary rounded-pill ms-2';
        span.textContent = cat.count;
        a.appendChild(span);
      }

      container.appendChild(a);
    });
  }

  var offcanvasEl = document.getElementById('categoriesOffcanvas');
  if (!offcanvasEl) return;

  offcanvasEl.addEventListener('show.bs.offcanvas', function(){
    if (populated) return;
    var dataEl = document.getElementById('categories-data');
    var raw = null;
    if (dataEl) raw = dataEl.textContent || dataEl.innerText || null;
    else if (window.CATEGORIES && Array.isArray(window.CATEGORIES)) raw = JSON.stringify(window.CATEGORIES);

    var categories = renderCategoriesList(raw);
    buildList(categories);
    populated = true;
  });
})();