(function ppt() {
  var nodes = document.querySelector(".ppt")
  var slides= nodes.getElementsByClassName('slide')
  var dots = nodes.getElementsByClassName("dot")
  var index =0
  var delay
  let i
  showSlide()
  function showSlide() {
    for (i=0; i<slides.length; i++) {
      slides[i].style.display = "none"
    }
    for (i=0; i< dots.length;i++) {
      dots[i].className = dots[i].className.replace(" active","")
    }
    index++
    if (index > slides.length) { index=1 }
    slides[index-1].style.display = "block"
    dots[index-1].className = dots[index-1].className + " active"
    delay = setTimeout(showSlide, 2000)
  }
  (function () {
    for (let i=0;i< dots.length;i++) {
      dots[i].addEventListener("click",function () {clickdot(i)})
    }
  }())
  function clickdot(n) {
    clearTimeout(delay)
    index = n
    showSlide()
  }
} () );
// 精品栏目
(function jplm() {
  var list = document.getElementsByTagName("dl")
  for (let i=0; i<list.length; i++) {
    list[i].onmouseover = fk 
  }
  function fk() {
    var showoff = document.getElementsByClassName("showUp")
    showoff[0].classList.toggle("showUp")
    var showOn = this.getElementsByTagName("div")
    showOn[0].classList.toggle("showUp")
  }
} () );
(function cft () {
  //get data
  var data = {
    l_ct: 10,
    r_ct: 90,
    l_num : 10,
    r_num : 90,
  }
  //animation
  var ct_bar = document.querySelectorAll('div[class$="count"]')
  var per = document.getElementsByClassName("per")
  var btn_count = function (node, count) {
    for (let i=1;i<count+1;i++) {
      setTimeout(function () {
        node.innerHTML= i + "%"
      }, 50*i)}
  }
  btn_count(per[0], data.l_ct)
  btn_count(per[1], data.r_ct)
  
  var bar_count = function (node, count) {
    for (let i=1;i<count+1;i++) {
      setTimeout(function () {
        node.style.width = 2*i + "px"
      }, 50*i)}
  }
  bar_count(ct_bar[0],data.l_num)
  bar_count(ct_bar[1],data.r_num)
  // button function
  document.querySelector("div.l-btn a").onclick = function () {
    var num = document.querySelector("div.left div.num");
    num.innerHTML = Number(num.innerHTML) + 1
  }
  document.querySelector("div.r-btn a").onclick = function () {
    var num = document.querySelector("div.right div.num");
    num.innerHTML = Number(num.innerHTML) + 1
  }
} ());
// 切换栏目函数
(function () {
  function slide(node) {
    var index = node.getElementsByClassName("title")[0].children
    var collection = node.getElementsByClassName("kuai")
    console.log(index.length,collection.length)
    function hover () {
      node.querySelector(".current").classList.toggle("current")
      node.querySelector(".now").classList.toggle("now")
      this.classList.toggle("current")
      for (var i=0;i<index.length;i++) {
        console.log(index[i].classList.contains("current"))
        if (index[i].classList.contains("current")) {
          console.log(i)
          collection[i].classList.toggle("now")
        }
      }
    }
    for (var i=0;i<index.length;i++) {
      index[i].onmouseover = hover
    }
  }
  var node = document.getElementsByClassName("slides")
  for (var i=0;i<node.length;i++) {
    slide(node[i])
  }
} () );
//看房幻灯片切换
(function () {
  function prev () {
    var node = document.querySelector(".scwr")
    node.firstElementChild.classList.toggle("split1")
    node.insertBefore(node.removeChild(node.lastElementChild), node.firstElementChild)
    node.firstElementChild.classList.toggle("split1")
  }
  function next () {
    var node = document.querySelector(".scwr")
    node.firstElementChild.classList.toggle("split1")
    node.appendChild(node.removeChild(node.firstElementChild))
    node.firstElementChild.classList.toggle("split1")
  }
  document.querySelector(".sr .next").onclick = next
  document.querySelector(".sr .prev").onclick = prev 
  setInterval(next, 7000)
} () );
//掌上大湘网
(function () {
  var node = document.querySelector(".zsdxw")
  node.onmouseover = function (e) {
    if (e.target.nodeName.toLowerCase() == "div" && e.target.classList != "zsdxw") {
      for (var i=0;i<3;i++) {
       node.children[i].firstElementChild.style.opacity = 0 
      }
      console.log(e.target)
      e.target.style.opacity = 1
    }
  }
} () );
//网站地图动画
(function () {
  document.querySelector(".webmap .hd").onclick = function () {
    var show = document.querySelector(".webmap .bd").style.height
    console.log(show)
    if (show != "0px" && show != "") {
      document.querySelector(".webmap .bd").style.height = "0"
      document.querySelector(".webmap .hd .arr").style.transform = "rotate(0deg)"
    }
    else {
      document.querySelector(".webmap .hd .arr").style.transform = "rotate(180deg)"
      document.querySelector(".webmap .bd").style.height = "634px"
    }
  }
} () );
(function () {
  document.querySelector(".fixnav").onclick = function (e) {
    if (e.target.nodeName.toLowerCase() == "a") {
      if (window.scrollTo) {
        e.preventDefault()
        var long
        var target = document.getElementById(e.target.getAttribute("href").substring(1))
        if (target == null) {
          long = 0
        } else {
          long = target.offsetTop
        }
        window.scrollTo({"behavior" : "smooth" , "top" : long});
        document.querySelector(".fixnav .current").classList.toggle("current")
        e.target.classList.toggle("current")
      }
    }
  }
    var data = document.querySelectorAll(".fixnav a")
    var distance = [0]
    for (var i=1;i<data.length-1;i++) {
      var tmp = document.getElementById(data[i].getAttribute("href").substring(1))
      distance.push(tmp.offsetTop-document.documentElement.clientWidth/4)
      console.log(tmp.offsetTop,)
    }
    window.addEventListener("scroll", function () {
    var currentLth = document.body.scrollTop+document.documentElement.scrollTop
    var test = function (site=0) {
      if (currentLth >= distance[site]) {
        var x = site + 1
        return test(x) 
      } else {
        var y = site -1
        return y 
      }
    }
    document.querySelector(".fixnav .current").classList.toggle("current")
    data[test()].classList.toggle("current")
  })
} ());
