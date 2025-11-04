(function () {
  function buildRows(element) {
    if (!element) {
      return [];
    }
    var rows = [];
    var currentRow = [];
    var nodes = element.childNodes;
    for (var i = 0; i < nodes.length; i++) {
      var node = nodes[i];
      if (node.nodeType === 1 && node.tagName === 'SPAN') {
        currentRow.push(node);
      } else if (node.nodeType === 1 && node.tagName === 'BR') {
        if (currentRow.length) {
          rows.push(currentRow);
          currentRow = [];
        }
      }
    }
    if (currentRow.length) {
      rows.push(currentRow);
    }
    return rows;
  }

  function applyWave(rows, calculator) {
    var height = rows.length;
    if (!height || typeof calculator !== 'function') {
      return;
    }
    for (var y = 0; y < height; y++) {
      var row = rows[y];
      var width = row.length || 1;
      for (var x = 0; x < width; x++) {
        var span = row[x];
        var delaySeconds = calculator(x, y, width, height);
        span.style.animationDelay = '-' + delaySeconds + 's';
      }
    }
  }

  function flattenRows(rows) {
    var flattened = [];
    for (var i = 0; i < rows.length; i++) {
      var row = rows[i];
      for (var j = 0; j < row.length; j++) {
        flattened.push(row[j]);
      }
    }
    return flattened;
  }

  function resolveDuration(element, fallback) {
    var raw = element.getAttribute('data-ripple-duration');
    var parsed = raw ? parseFloat(raw) : NaN;
    if (!isFinite(parsed) || parsed <= 0) {
      return fallback;
    }
    return parsed;
  }

  function applyEndlessRipple(element) {
    var rows = buildRows(element);
    if (!rows.length) {
      return;
    }
    var spans = flattenRows(rows);
    var totalSpans = spans.length;
    if (!totalSpans) {
      return;
    }
    var duration = resolveDuration(element, 3.0);
    var step = duration / totalSpans;
    var baseDelay = step;
    for (var index = 0; index < totalSpans; index++) {
      var delaySeconds = baseDelay + index * step;
      spans[index].style.animationDelay = '-' + delaySeconds.toFixed(3) + 's';
    }
  }

  var calculators = {
    'sine-flow': function (x, y, width) {
      var divisor = Math.max(1, width);
      var amplitude = Math.sin(((x + y) / divisor) * Math.PI / 2.0);
      return amplitude * 3.0;
    },
    'pin-grid': function (x, y, width, height) {
      var divisorX = Math.max(1, width);
      var divisorY = Math.max(1, height);
      var amplitude =
        Math.sin(-(x - divisorX / 4.0) / divisorX * Math.PI) *
        Math.sin(-(y - divisorY / 4.0) / divisorY * Math.PI);
      return amplitude * 3.0;
    },
    'offset-columns': function (x, y, width, height) {
      if (width <= 1 && height <= 1) {
        return 0;
      }
      var normalizedX = width > 1 ? x / (width - 1) : 0;
      var normalizedY = height > 1 ? y / (height - 1) : 0;
      var phase = (normalizedX + normalizedY) * Math.PI;
      return Math.sin(phase - Math.PI / 2) * 2.5;
    }
  };

  function initialiseWaves() {
    var targets = document.querySelectorAll('[data-wave]');
    targets.forEach(function (element) {
      var mode = element.getAttribute('data-wave');
      var calculator = calculators[mode];
      if (!calculator) {
        return;
      }
      var rows = buildRows(element);
      applyWave(rows, calculator);
    });
  }

  function initialiseRipples() {
    var rippleTargets = document.querySelectorAll('.anim1_5');
    rippleTargets.forEach(function (element) {
      applyEndlessRipple(element);
    });
  }

  function initialise() {
    initialiseWaves();
    initialiseRipples();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initialise);
  } else {
    initialise();
  }
})();
