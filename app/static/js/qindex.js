webpackJsonp([0],[,function(t,e,n){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var i=n(2),s=(n.n(i),n(3)),o=(n.n(s),n(4));n.n(o)},function(t,e,n){(function(t){t(document).ready(function(){!function(){t(".ppt").each(function(e){var n=1,i=t(".slide"),s=t(".dot");function o(){i.siblings().hide(),i.eq(n).fadeIn(),s.removeClass("active").eq(n).addClass("active"),(n+=1)==i.length&&(n=0)}s.on("click",function(e){t(this).addClass("active").siblings().removeClass("active"),n=t(this).index(),o()}),setInterval(o,7e3)})}(),t("dl").delegate("dt","mouseenter",function(){t(this).next().show().siblings("dd").hide()}),t.get("/api/question",function(e){function n(e,n){var i=t(e);t({Counter:0}).animate({Counter:n},{duration:50*n,easing:"swing",step:function(){i.text(Math.ceil(this.Counter)+"%")}})}t(".cft .question").text(e.title).next().text(e.detail),t(".cft .left .num").text(e.yes),t(".cft .right .num").text(e.no),n(".cft .left .per",e.yesper),n(".cft .right .per",e.noper),t(".cft .left .lcount").animate({width:2*e.yesper+"px"},50*e.yesper),t(".cft .right .rcount").animate({width:2*e.noper+"px"},50*e.noper)}),t(".cft .per").one("click",function(){var e=t(this).parent().siblings(".num");e.text(Number(e.text())+1),t(".cft .per").css("cursor","auto").unbind().on("click",function(){alert("你已经投过票了")})}),t(".slides").each(function(){var e=t(this).find(".title"),n=t(this).find(".kuai");e.delegate("li","mouseover",function(){t(this).addClass("current").siblings().removeClass("current");var i=e.find("li").index(this);n.removeClass("now").eq(i).addClass("now")})}),t(".next").click(function(){t(".scwr .split:first").toggleClass("split1").remove().appendTo(".scwr"),t(".scwr .split:first").toggleClass("split1")}),t(".prev").click(function(){t(".scwr .split:last").toggleClass("split1").remove().insertBefore(".split:first"),t(".scwr .split").eq(1).toggleClass("split1")}),t(".webmap .hd").click(function(){t(".webmap .bd").toggleClass("boom"),t(".webmap .hd .arr").toggleClass("boom7")}),function(e){var n={};t(e).children().not(".top").each(function(){console.log(this);var i=t(t(this).attr("href")).offset().top;n[e+" ."+t(this).attr("href").slice(1)]=i,console.log(n)}).on("click",function(){var e=t(t(this).attr("href")).offset().top;t("html, body").animate({scrollTop:e}),event.preventDefault()}),t(".top").on("click",function(){t("html, body").animate({scrollTop:0}),event.preventDefault()}),setInterval(function(){var e,i=.5*t(window).height();for(var s in current_top=t(window).scrollTop(),console.log(current_top),n)n[s]-i<=current_top&&(e=s);t(e).addClass("current").siblings().removeClass("current")},250)}(".fixnav")})}).call(e,n(0))},function(t,e){},function(t,e){}],[1]);