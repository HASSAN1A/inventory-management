// ========== TOGGLE SIDEBAR ==========
let menuIcon = $("i#menu");
let closeIcon = $("i#close");
let sidebar = $("div#sidebar");
let main = $('div.main-bar');
let spill  = $('div#sidebar-spill');

window.onresize = ()=>{
  if($(window).width() > 768){
    sidebar.css('left', 0);
    spill.hide()
  } else {
      sidebar.css('left', '-15rem')
  }
}

menuIcon.on("click", function () {
  sidebar.animate({ left: "0" }, 200);
  main.css('overflow', 'hidden');
  spill.fadeIn(300)

});

closeIcon.on("click", function () {
  sidebar.animate({ left: "-15rem" }, 200);
  spill.fadeOut(300);
});

spill.on("click", function () {
  sidebar.animate({ left: "-15rem" }, 200);
  spill.fadeOut(300);
});
