(function () {
  "use strict";

  function linksFrom(slot) {
    var q = "server=" + slot.server + "&port=" + slot.port + "&secret=" + slot.secret;
    return {
      tg: slot.tg_link || "tg://proxy?" + q,
      https: slot.https_link || "https://t.me/proxy?" + q
    };
  }

  function applySlot(slot) {
    if (!slot || !slot.server || !slot.port || !slot.secret) return;
    var links = linksFrom(slot);
    var nodes = document.querySelectorAll("[data-proxy-slot]");
    var i;
    for (i = 0; i < nodes.length; i++) {
      var el = nodes[i];
      var kind = el.getAttribute("data-proxy-kind") || "tg";
      el.setAttribute("href", kind === "https" ? links.https : links.tg);
    }
    var status = document.getElementById("proxy-status");
    if (status) {
      var dead = slot.alive === false;
      status.dataset.state = dead ? "dead" : "live";
      status.innerHTML = '<span class="dot" aria-hidden="true"></span> ' +
        (dead ? "слот обновляем" : "прокси на сайте живой");
    }
  }

  try {
    fetch("data/proxy.json", { cache: "no-store" }).then(function (res) {
      if (!res.ok) return null;
      return res.json();
    }).then(function (slot) {
      if (slot) applySlot(slot);
    }).catch(function () {
      /* file:// or blocked fetch: baked-in hrefs stay */
    });
  } catch (err) {
    /* ignore */
  }

  var buttons = document.querySelectorAll("[data-copy]");
  var b;
  for (b = 0; b < buttons.length; b++) {
    buttons[b].addEventListener("click", function (ev) {
      var value = ev.currentTarget.getAttribute("data-copy") || "VNESPISKA";
      var btn = ev.currentTarget;
      var done = function () {
        var prev = btn.textContent;
        btn.textContent = "Скопировано";
        setTimeout(function () { btn.textContent = prev; }, 1400);
      };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(value).then(done).catch(done);
      } else {
        done();
      }
    });
  }
})();
