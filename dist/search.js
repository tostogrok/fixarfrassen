(function () {
  "use strict";
  var q = document.getElementById("q");
  if (!q) return;
  var none = document.getElementById("q-none");
  function norm(s) { return String(s || "").toLowerCase().normalize("NFC"); }
  q.addEventListener("input", function () {
    var words = norm(q.value).split(/\s+/).filter(Boolean), shown = 0;
    document.querySelectorAll("#guider .grp").forEach(function (grp) {
      var visible = 0;
      grp.querySelectorAll(".cards a").forEach(function (a) {
        var hay = a.getAttribute("data-q") || "";
        var ok = words.every(function (w) { return hay.indexOf(w) >= 0; });
        a.hidden = !ok; if (ok) visible++;
      });
      grp.hidden = visible === 0; shown += visible;
    });
    none.hidden = shown > 0;
  });
}());
