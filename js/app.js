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

  function withUtm(href, campaign, content) {
    var url;
    try { url = new URL(href, location.href); } catch (e) { return href; }
    if (url.hostname !== "t.me" && url.hostname !== "magnit.help") return href;
    var params = new URLSearchParams(location.search);
    ["utm_source", "utm_medium", "utm_campaign", "utm_content"].forEach(function (key) {
      var val = params.get(key);
      if (val && !url.searchParams.get(key)) url.searchParams.set(key, val);
    });
    if (!url.searchParams.get("utm_source")) url.searchParams.set("utm_source", "goida");
    if (!url.searchParams.get("utm_medium")) url.searchParams.set("utm_medium", "site");
    if (campaign && !url.searchParams.get("utm_campaign")) url.searchParams.set("utm_campaign", campaign);
    if (content && !url.searchParams.get("utm_content")) url.searchParams.set("utm_content", content);
    return url.toString();
  }

  var links = document.querySelectorAll('a[href*="t.me/"], a[href*="magnit.help"]');
  var i;
  for (i = 0; i < links.length; i++) {
    links[i].setAttribute(
      "href",
      withUtm(
        links[i].getAttribute("href"),
        links[i].getAttribute("data-utm-campaign"),
        links[i].getAttribute("data-utm-content")
      )
    );
  }

  var sticky = document.querySelector(".sticky");
  if (sticky) {
    var onScroll = function () {
      if (window.scrollY > 400) sticky.removeAttribute("hidden");
      else sticky.setAttribute("hidden", "");
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  document.addEventListener("click", function (ev) {
    var el = ev.target.closest("[data-track]");
    if (!el) return;
    track(el.getAttribute("data-track"));
  });

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

  var shout = document.getElementById("goida-shout");
  var audio = document.getElementById("goida-audio");
  if (shout) {
    shout.addEventListener("click", function (ev) {
      if (ev && ev.preventDefault) ev.preventDefault();
      track("goida_shout");
      if (audio) {
        audio.currentTime = 0;
        var play = audio.play();
        if (play && typeof play.catch === "function") {
          play.catch(function () {});
        }
      }
      shout.classList.remove("is-yell");
      shout.style.animation = "none";
      window.requestAnimationFrame(function () {
        shout.style.animation = "";
        shout.classList.add("is-yell");
      });
    });
  }

  var analyticsLoaded = false;
  function loadAnalytics() {
    if (analyticsLoaded) return;
    analyticsLoaded = true;
    var ymId = window.GOIDA_YM || 112149595;
    var gaId = window.GOIDA_GA || "G-KCKYM27XVJ";
    var metrika = document.createElement("script");
    metrika.src = "https://mc.yandex.ru/metrika/tag.js?id=" + ymId;
    metrika.async = true;
    metrika.onload = function () {
      if (typeof window.ym === "function") {
        window.ym(ymId, "init", {
          ssr: true,
          webvisor: true,
          clickmap: true,
          accurateTrackBounce: true,
          trackLinks: true,
          ecommerce: "dataLayer"
        });
      }
    };
    document.head.appendChild(metrika);
    var ga = document.createElement("script");
    ga.src = "https://www.googletagmanager.com/gtag/js?id=" + gaId;
    ga.async = true;
    ga.onload = function () {
      gtag("js", new Date());
      gtag("config", gaId);
    };
    document.head.appendChild(ga);
  }
  ["click", "scroll", "touchstart", "keydown"].forEach(function (name) {
    window.addEventListener(name, loadAnalytics, { once: true, passive: true });
  });
  window.setTimeout(loadAnalytics, 12000);
})();
