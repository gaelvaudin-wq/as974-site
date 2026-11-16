/* Active Sécurité 974 — JS vanilla, sans dépendance. */
(function(){
  "use strict";
  var d=document, root=d.documentElement;
  root.classList.add("js");
  var KEY="as974-devis";
  var reduce=window.matchMedia&&window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function $(s,c){return (c||d).querySelector(s)}
  function $$(s,c){return Array.prototype.slice.call((c||d).querySelectorAll(s))}
  function norm(s){return (s||"").toString().toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g,"").trim()}
  function esc(s){return (s||"").replace(/[&<>"]/g,function(c){return{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]})}

  /* ---------- menu mobile + sous-menus ---------- */
  var toggle=$(".menu-toggle"), nav=$("#site-nav");
  if(toggle&&nav){
    toggle.addEventListener("click",function(){
      var open=!d.body.classList.contains("menu-open");
      d.body.classList.toggle("menu-open",open);
      toggle.setAttribute("aria-expanded",open?"true":"false");
      toggle.setAttribute("aria-label",open?"Fermer le menu":"Ouvrir le menu");
    });
    d.addEventListener("keydown",function(e){
      if(e.key==="Escape"&&d.body.classList.contains("menu-open")){toggle.click();toggle.focus()}
    });
  }
  $$(".nav-drop").forEach(function(dd){
    var b=$("button",dd), t;
    function set(o){dd.classList.toggle("open",o);b.setAttribute("aria-expanded",o?"true":"false")}
    b.addEventListener("click",function(e){e.stopPropagation();set(!dd.classList.contains("open"))});
    dd.addEventListener("mouseenter",function(){if(window.innerWidth>980){clearTimeout(t);set(true)}});
    dd.addEventListener("mouseleave",function(){if(window.innerWidth>980){t=setTimeout(function(){set(false)},150)}});
    dd.addEventListener("keydown",function(e){if(e.key==="Escape"){set(false);b.focus()}});
    dd.addEventListener("focusout",function(e){if(!dd.contains(e.relatedTarget)&&window.innerWidth>980)set(false)});
    d.addEventListener("click",function(e){if(!dd.contains(e.target))set(false)});
  });

  /* ---------- apparition au scroll ---------- */
  var rv=$$(".reveal");
  if(!reduce&&"IntersectionObserver" in window){
    var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add("in");io.unobserve(e.target)}})},{rootMargin:"0px 0px -8% 0px",threshold:.08});
    rv.forEach(function(el){io.observe(el)});
  } else rv.forEach(function(el){el.classList.add("in")});

  /* ---------- rails ---------- */
  $$("[data-rail]").forEach(function(wrap){
    var rail=$(".rail",wrap), prev=$("[data-prev]",wrap), next=$("[data-next]",wrap);
    if(!rail||!prev||!next)return;
    function upd(){prev.disabled=rail.scrollLeft<8;next.disabled=rail.scrollLeft+rail.clientWidth>=rail.scrollWidth-8}
    function go(dir){rail.scrollBy({left:dir*rail.clientWidth*.85,behavior:reduce?"auto":"smooth"})}
    prev.addEventListener("click",function(){go(-1)});next.addEventListener("click",function(){go(1)});
    rail.addEventListener("scroll",upd,{passive:true});window.addEventListener("resize",upd);upd();
  });

  /* ---------- sélection devis (localStorage) ---------- */
  function load(){try{return JSON.parse(localStorage.getItem(KEY))||[]}catch(e){return[]}}
  function save(l){try{localStorage.setItem(KEY,JSON.stringify(l))}catch(e){}updCount()}
  function updCount(){var n=load().length;$$(".sl-count").forEach(function(c){c.textContent=n;c.hidden=!n});$$(".sl-label").forEach(function(c){c.textContent=n?"Ma sélection devis ("+n+" produit"+(n>1?"s":"")+")":"Ma sélection devis"})}
  function has(s){return load().some(function(i){return i.s===s})}
  function toast(msg){var t=$(".toast");if(!t){t=d.createElement("div");t.className="toast";t.setAttribute("role","status");t.setAttribute("aria-live","polite");d.body.appendChild(t)}t.innerHTML=msg;t.classList.add("show");clearTimeout(t._h);t._h=setTimeout(function(){t.classList.remove("show")},3200)}
  updCount();
  d.addEventListener("click", function(e){
    var b=e.target.closest&&e.target.closest(".yt-btn");
    if(!b)return;
    var fig=b.closest(".yt"), id=fig&&fig.getAttribute("data-yt");
    if(!id)return;
    var f=d.createElement("iframe");
    f.className="yt-frame";
    f.src="https://www.youtube-nocookie.com/embed/"+encodeURIComponent(id)+"?autoplay=1&rel=0";
    f.title=b.getAttribute("aria-label")||"Vidéo Ajax Systems";
    f.setAttribute("allow","accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share");
    f.setAttribute("allowfullscreen","");
    f.setAttribute("loading","lazy");
    b.replaceWith(f);
  });
  window.AS974={load:load,save:save,toast:toast};

  /* ---------- filtres catalogue ---------- */
  var cat=$("[data-catalogue]");
  if(cat){
    var cards=$$(".prod",cat), q=$("#f-q"), fg=$("#f-gamme"), fs=$("#f-sous"), fc=$("#f-couleur"), fgr=$("#f-groupe"), count=$("#f-count"), empty=$("#f-empty"), reset=$("#f-reset");
    var params=new URLSearchParams(location.search);
    function setSel(el,k){if(el&&params.get(k)){var v=params.get(k);if($$("option",el).some(function(o){return o.value===v}))el.value=v}}
    if(q&&params.get("q"))q.value=params.get("q");
    setSel(fg,"gamme");setSel(fs,"sous");setSel(fc,"couleur");setSel(fgr,"groupe");
    var more=$("#f-more"), pageSize=24, shownMax=24;
    function narrow(){return window.matchMedia("(max-width:700px)").matches}
    function apply(push){
      if(push)shownMax=pageSize;
      var qv=norm(q&&q.value), gv=fg?fg.value:"", sv=fs?fs.value:"", cv=fc?fc.value:"", grv=fgr?fgr.value:"", n=0, kept=0;
      cards.forEach(function(c){
        var ok=(!qv||c.dataset.q.indexOf(qv)>-1)&&(!gv||c.dataset.g===gv)&&(!sv||c.dataset.c===sv)&&(!cv||("|"+c.dataset.col+"|").indexOf("|"+cv+"|")>-1)&&(!grv||c.dataset.grp===grv);
        if(!ok){c.hidden=true;return}
        n++;
        if(narrow()&&kept>=shownMax){c.hidden=true;return}
        c.hidden=false; kept++;
      });
      if(more)more.hidden=!(narrow()&&n>shownMax);
      if(count)count.textContent=n+" référence"+(n>1?"s":"")+(n===cards.length?"":" sur "+cards.length);
      if(empty)empty.hidden=n>0;
      if(push&&history.replaceState){
        var p=new URLSearchParams();
        if(q&&q.value)p.set("q",q.value);if(gv)p.set("gamme",gv);if(sv)p.set("sous",sv);if(cv)p.set("couleur",cv);if(grv)p.set("groupe",grv);
        history.replaceState(null,"",location.pathname+(p.toString()?"?"+p:"")+location.hash);
      }
    }
    [q,fg,fs,fc,fgr].forEach(function(el){if(el)el.addEventListener(el.tagName==="INPUT"?"input":"change",function(){apply(true)})});
    if(reset)reset.addEventListener("click",function(){if(q)q.value="";shownMax=pageSize;[fg,fs,fc,fgr].forEach(function(el){if(el)el.value=""});apply(true)});
    if(more)more.addEventListener("click",function(){shownMax+=pageSize;apply(false);more.focus()});
    apply(false);
  }

  /* ---------- fiche produit : couleur + devis + sélection ---------- */
  var pdpData=$("#pdp-data");
  if(pdpData){
    var P=JSON.parse(pdpData.textContent), img=$("#pdp-img"), src=$("#pdp-src"), out=$("#pdp-color-name"), quote=$("#pdp-quote"), addb=$("#pdp-add");
    var current=P.default||"";
    var pc=new URLSearchParams(location.search).get("couleur");
    if(pc&&P.images[pc])current=pc;
    function quoteUrl(){var p=new URLSearchParams();p.set("produit",P.slug);p.set("modele",P.name);if(P.ref)p.set("ref",P.ref);if(current)p.set("couleur",current);return P.contact+"?"+p.toString()+"#devis"}
    function setColor(c,anim){
      current=c;
      if(out)out.textContent=c;
      var im=P.images[c];
      if(im&&img){
        var doSwap=function(){if(src)src.srcset=im.webp;img.src=im.png;img.style.setProperty("--w",im.w+"px");img.width=im.w;img.height=im.h;img.alt=P.name+" — coloris "+c;img.dataset.color=c};
        if(anim&&!reduce){img.classList.add("swap");setTimeout(function(){doSwap();img.onload=function(){img.classList.remove("swap")};setTimeout(function(){img.classList.remove("swap")},350)},150)}else doSwap();
      }
      $$(".js-quote").forEach(function(a){a.href=quoteUrl()});
      var r=$('input[name="couleur"][value="'+CSS.escape(c)+'"]');if(r)r.checked=true;
      if(history.replaceState&&c){var u=new URL(location.href);u.searchParams.set("couleur",c);history.replaceState(null,"",u)}
    }
    $$('input[name="couleur"]').forEach(function(r){r.addEventListener("change",function(){setColor(r.value,true)})});
    var variant=$("#pdp-variant");
    if(variant) variant.addEventListener("change",function(){
      var url=variant.value; if(!url) return;
      if(current) url+=(url.indexOf("?")>=0?"&":"?")+"couleur="+encodeURIComponent(current);
      location.href=url;
    });
    if(current)setColor(current,false); else $$(".js-quote").forEach(function(a){a.href=quoteUrl()});
    function updAdd(){if(!addb)return;var on=has(P.slug);addb.setAttribute("aria-pressed",on?"true":"false");addb.textContent=on?"Dans ma sélection devis ✓":"Ajouter à ma sélection devis"}
    if(addb){addb.addEventListener("click",function(){
      var l=load(),i=l.findIndex(function(x){return x.s===P.slug});
      if(i>-1){l.splice(i,1);save(l);toast("Retiré de votre sélection.")}
      else{l.push({s:P.slug,n:P.name,r:P.ref||"",c:current||""});save(l);toast("Ajouté à votre sélection devis.<a href=\""+P.contact+"#devis\">Voir</a>")}
      updAdd();
    });updAdd();}
  }

  /* ---------- formulaire devis : préremplissage ---------- */
  var form=$("#form-devis");
  var prAll=new URLSearchParams(location.search), banner=$("#prefill");
  if(banner && !form){
    var modele0=prAll.get("modele"), ref0=prAll.get("ref"), coul0=prAll.get("couleur");
    if(modele0){banner.innerHTML="Vous regardiez <strong>"+esc(modele0)+"</strong>"+(ref0?" (réf. "+esc(ref0)+")":"")+(coul0?" — coloris <strong>"+esc(coul0)+"</strong>":"")+".";banner.classList.add("show")}
  }
  if(form){
    var pr=prAll, list=$("#sl-list"), ta=$("#f-produits");
    var modele=pr.get("modele"), ref=pr.get("ref"), coul=pr.get("couleur"), slug=pr.get("produit");
    if(modele&&slug){
      var l=load(), ex=l.find(function(x){return x.s===slug});
      if(ex){if(coul)ex.c=coul}else l.unshift({s:slug,n:modele,r:ref||"",c:coul||""});
      save(l);
      if(banner){banner.innerHTML="Demande de devis pour <strong>"+esc(modele)+"</strong>"+(ref?" (réf. "+esc(ref)+")":"")+(coul?" — coloris <strong>"+esc(coul)+"</strong>":"")+". Complétez vos coordonnées ci-dessous.";banner.classList.add("show")}
    }
    var prof=pr.get("profil"); if(prof){var ps=$("#f-profil");if(ps){$$("option",ps).forEach(function(o){if(norm(o.value)===norm(prof))ps.value=o.value})}}
    function line(i){return i.n+(i.r?" (réf. "+i.r+")":"")+(i.c?" — coloris : "+i.c:"")}
    function render(){
      var l=load();
      if(ta){ta.value=l.map(line).join("\n")}
      if(!list)return;
      if(!l.length){list.innerHTML='<li class="sl-empty">Aucun produit pour l’instant. Ajoutez-en depuis le catalogue.</li>';return}
      list.innerHTML=l.map(function(i,k){return '<li><span>'+esc(line(i))+'</span><button type="button" data-rm="'+k+'" aria-label="Retirer '+esc(i.n)+'">Retirer</button></li>'}).join("");
      $$("[data-rm]",list).forEach(function(b){b.addEventListener("click",function(){var l=load();l.splice(+b.dataset.rm,1);save(l);render()})});
    }
    render();
    form.addEventListener("submit",function(e){
      if(!form.checkValidity()){e.preventDefault();form.reportValidity();return}
      var action=form.getAttribute("action")||"";
      var ready=/^https?:\/\//i.test(action);
      if(!ready){
        e.preventDefault();
        var fd=new FormData(form), lines=[];
        fd.forEach(function(v,k){if(k==="_gotcha"||k==="_subject"||k==="bot-field")return; if(String(v).trim()) lines.push(k+" : "+v)});
        var mail=form.getAttribute("data-mailto")||"";
        if(mail.indexOf("@")<0){return}
        var subject=encodeURIComponent("Demande de devis — Active Sécurité 974");
        var body=encodeURIComponent(lines.join("\n"));
        window.location.href="mailto:"+mail+"?subject="+subject+"&body="+body;
        return;
      }
      try{localStorage.removeItem(KEY)}catch(x){}
    });
  }
  /* ---------- vidéos : autoplay hero, lecture à l'arrivée, reduced-motion ---------- */
  $$("video.js-video").forEach(function(v){
    if(reduce){v.removeAttribute("autoplay"); try{v.pause()}catch(e){} return}
    var start=function(){var p=v.play(); if(p&&p.catch)p.catch(function(){})};
    if(v.classList.contains("is-hero")){start(); return}
    if(!("IntersectionObserver" in window)) return;
    var io=new IntersectionObserver(function(es){
      es.forEach(function(e){ if(e.isIntersecting) start(); else v.pause(); });
    },{threshold:.5});
    io.observe(v);
  });

  /* ---------- quotidien : l'écran suit l'étape visible ---------- */
  var day=document.querySelector("[data-day]");
  if(day){
    var steps=$$("li", day), phone=document.querySelector(".phone");
    function show(i){
      steps.forEach(function(s,k){s.classList.toggle("is-on", k===i)});
      if(phone) phone.setAttribute("data-on", String(i));
    }
    if(reduce || !("IntersectionObserver" in window)) show(0);
    else {
      var dio=new IntersectionObserver(function(es){
        es.forEach(function(e){ if(e.isIntersecting) show(steps.indexOf(e.target)); });
      },{threshold:.6});
      steps.forEach(function(s){dio.observe(s)});
    }
  }

  /* ---------- configurateur LightSwitch / Outlet ---------- */
  var cfg=document.getElementById("cfg"), cfgData=document.getElementById("cfg-data");
  if(cfg && cfgData){
    var C=JSON.parse(cfgData.textContent);
    var seats=document.getElementById("cfg-seats"), slots=document.getElementById("cfg-slots");
    var stage=document.getElementById("cfg-stage"), cname=document.getElementById("cfg-color-name");
    var color="Blanc";
    function devs(){return C.devices}
    function paint(){
      var n=+seats.value, html="", imgs="";
      for(var i=0;i<n;i++){
        var opts=devs().map(function(d,ix){return '<option value="'+ix+'"'+(ix===Math.min(i,devs().length-1)?'':'')+'>'+esc(d.name)+'</option>'}).join("");
        html+='<label>Poste '+(i+1)+' <select class="cfg-slot">'+opts+'</select></label>';
      }
      slots.innerHTML=html;
      $$(".cfg-slot", slots).forEach(function(sel,i){ sel.selectedIndex=Math.min(i, sel.options.length-1); sel.addEventListener("change", draw); });
      draw();
    }
    function draw(){
      var parts=[], imgs="";
      $$(".cfg-slot", slots).forEach(function(sel){
        var d=devs()[+sel.value]; if(!d) return;
        var src=d.images[color]||d.images.Blanc||"";
        parts.push(d.name+" — "+color+(d.model?" (réf. "+d.model+")":""));
        if(src) imgs+='<figure><img src="'+src+'" alt="'+esc(d.name+" "+color)+'"><figcaption>'+esc(d.name)+'</figcaption></figure>';
      });
      stage.innerHTML=imgs||"<p>Visuel non disponible pour ce coloris.</p>";
      cfg._parts=parts;
    }
    $$(".cfg-color", cfg).forEach(function(b){
      b.addEventListener("click", function(){
        color=b.getAttribute("data-color");
        $$(".cfg-color", cfg).forEach(function(x){x.setAttribute("aria-pressed", x===b?"true":"false")});
        var meta=C.colors.filter(function(c){return c.name===color})[0];
        if(cname&&meta) cname.textContent=meta.name+" · "+meta.ral+". Le RAL est une approximation indiquée par Ajax.";
        draw();
      });
    });
    seats.addEventListener("change", paint);
    paint();
    var qbtn=document.getElementById("cfg-quote");
    if(qbtn) qbtn.addEventListener("click", function(){
      var l=load();
      (cfg._parts||[]).forEach(function(label){
        var d=devs().filter(function(x){return label.indexOf(x.name)===0})[0];
        if(!d) return;
        l.push({s:d.slug,n:d.name+" ("+color+")",r:d.model||"",c:color});
      });
      save(l);
      location.href="contact.html#devis";
    });
  }
})();
