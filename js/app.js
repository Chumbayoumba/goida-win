(function () {
  "use strict";

  function track(name, extra) {
    var payload = { event: name };
    if (extra) {
      var k;
      for (k in extra) {
        if (Object.prototype.hasOwnProperty.call(extra, k)) payload[k] = extra[k];
      }
    }
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push(payload);
    if (typeof window.gtag === "function") {
      window.gtag("event", name, extra || {});
    }
    if (typeof window.ym === "function") {
      window.ym(112149595, "reachGoal", name);
    }
  }

  track("page_view", {
    hero: /(?:\?|&)hero=b(?:&|$)/.test(location.search) ? "b" : "a",
    utm_source: (location.search.match(/utm_source=([^&]+)/) || [])[1] || "",
    utm_campaign: (location.search.match(/utm_campaign=([^&]+)/) || [])[1] || ""
  });

  if (/(?:\?|&)hero=b(?:&|$)/.test(location.search)) {
    var title = document.getElementById("hero-title");
    var lead = document.getElementById("hero-lead");
    if (title) title.textContent = "Интернет опять решили сломать?";
    if (lead) lead.innerHTML = "Telegram → прокси.<br>YouTube, сайты, WhatsApp → VPN.";
  }

  function withUtm(href) {
    var url;
    try { url = new URL(href, location.href); } catch (e) { return href; }
    if (url.hostname !== "t.me") return href;
    var params = new URLSearchParams(location.search);
    ["utm_source", "utm_medium", "utm_campaign", "utm_content"].forEach(function (key) {
      var val = params.get(key);
      if (val && !url.searchParams.get(key)) url.searchParams.set(key, val);
    });
    if (!url.searchParams.get("utm_source")) url.searchParams.set("utm_source", "goida");
    if (!url.searchParams.get("utm_medium")) url.searchParams.set("utm_medium", "site");
    return url.toString();
  }

  var links = document.querySelectorAll('a[href*="t.me/"]');
  var i;
  for (i = 0; i < links.length; i++) {
    links[i].setAttribute("href", withUtm(links[i].getAttribute("href")));
  }

  document.addEventListener("click", function (ev) {
    var el = ev.target.closest("[data-track]");
    if (!el) return;
    track(el.getAttribute("data-track"));
  });

  function linksFrom(slot) {
    var q = "server=" + slot.server + "&port=" + slot.port + "&secret=" + slot.secret;
    return {
      tg: slot.tg_link || "tg://proxy?" + q,
      https: slot.https_link || "https://t.me/proxy?" + q
    };
  }

  function applySlot(slot) {
    if (!slot || !slot.server || !slot.port || !slot.secret) return;
    var built = linksFrom(slot);
    var nodes = document.querySelectorAll("[data-proxy-slot]");
    var n;
    for (n = 0; n < nodes.length; n++) {
      var el = nodes[n];
      if (el.getAttribute("data-proxy-stub") === "1") continue;
      var kind = el.getAttribute("data-proxy-kind") || "tg";
      el.setAttribute("href", kind === "https" ? built.https : built.tg);
    }
  }

  try {
    fetch("data/proxy.json", { cache: "no-store" }).then(function (res) {
      if (!res.ok) return null;
      return res.json();
    }).then(function (slot) {
      if (slot) applySlot(slot);
    }).catch(function () {});
  } catch (err) {}

  var buttons = document.querySelectorAll("[data-copy]");
  var b;
  for (b = 0; b < buttons.length; b++) {
    buttons[b].addEventListener("click", function (ev) {
      var value = ev.currentTarget.getAttribute("data-copy") || "VNESPISKA";
      var btn = ev.currentTarget;
      var done = function () {
        btn.textContent = "Код скопирован";
        setTimeout(function () { btn.textContent = "Копировать"; }, 1600);
      };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(value).then(done).catch(done);
      } else {
        done();
      }
    });
  }
})();
