(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-31387dd1"],{"0653":function(t,e,n){"use strict";n("68ef")},"1f5b":function(t,e,n){},"34e9":function(t,e,n){"use strict";var i=n("2638"),a=n.n(i),s=n("a142"),o=n("ba31"),c=Object(s["g"])("cell-group"),r=c[0],l=c[1];function d(t,e,n,i){var s=t("div",a()([{class:[l(),{"van-hairline--top-bottom":e.border}]},Object(o["b"])(i,!0)]),[n.default&&n.default()]);return e.title?t("div",[t("div",{class:l("title")},[e.title]),s]):s}d.props={title:String,border:{type:Boolean,default:!0}},e["a"]=r(d)},4096:function(t,e,n){"use strict";n.r(e);var i=function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("div",{staticClass:"goods"},[n("van-swipe",{staticClass:"goods-swipe",attrs:{autoplay:3e3}},t._l(t.goods.thumb,function(t){return n("van-swipe-item",{key:t},[n("img",{attrs:{src:t}})])}),1),n("van-cell-group",[n("van-cell",[n("div",{staticClass:"goods-title"},[t._v(t._s(t.goods.title))]),n("div",{staticClass:"goods-price"},[t._v(t._s(t.formatPrice(t.goods.price)))])]),n("van-cell",{staticClass:"goods-express"},[n("van-col",{attrs:{span:"10"}},[t._v("运费："+t._s(t.goods.express))]),n("van-col",{attrs:{span:"14"}},[t._v("剩余："+t._s(t.goods.remain))])],1)],1),n("van-cell",{attrs:{title:"查看商品详情"}}),n("div",{staticClass:"detail",domProps:{innerHTML:t._s(t.goods.detail)}}),n("van-goods-action",[n("van-goods-action-mini-btn",{attrs:{icon:"wap-home",to:"/home"}},[t._v("\n      首页 \n    ")]),n("van-goods-action-mini-btn",{attrs:{icon:"cart-o",info:t.goodsNum},on:{click:t.onClickCart}},[t._v("\n      购物车\n    ")]),n("van-goods-action-big-btn",{on:{click:function(e){return t.additem(t.goods)}}},[t._v("\n      加入购物车\n    ")]),n("van-goods-action-big-btn",{attrs:{primary:""},on:{click:t.sorry}},[t._v("\n      立即购买\n    ")])],1)],1)},a=[],s=(n("7514"),n("e7e5"),n("d399")),o=n("bd86"),c=(n("68ef"),n("1f5b"),n("c31d")),r=n("2638"),l=n.n(r),d=n("a142"),u=n("ad06"),f=n("ba31"),b=n("48f4"),h=Object(d["g"])("goods-action-mini-btn"),p=h[0],m=h[1];function g(t,e,n,i){var a=function(t){Object(f["a"])(i,"click",t),Object(b["a"])(i)};return t("div",l()([{class:[m(),"van-hairline"],on:{click:a}},Object(f["b"])(i)]),[t(u["a"],{class:[m("icon"),e.iconClass],attrs:{tag:"div",info:e.info,name:e.icon}}),n.default?n.default():e.text])}g.props=Object(c["a"])({},b["c"],{text:String,icon:String,info:[String,Number],iconClass:null});var v=p(g),j=(n("5fbe"),n("b650")),O=Object(d["g"])("goods-action-big-btn"),w=O[0],x=O[1];function k(t,e,n,i){var a=function(t){Object(f["a"])(i,"click",t),Object(b["a"])(i)};return t(j["a"],l()([{attrs:{square:!0,size:"large",loading:e.loading,disabled:e.disabled,type:e.primary?"danger":"warning"},class:x(),on:{click:a}},Object(f["b"])(i)]),[n.default?n.default():e.text])}k.props=Object(c["a"])({},b["c"],{text:String,primary:Boolean,loading:Boolean,disabled:Boolean});var y=w(k),C=(n("4cf9"),Object(d["g"])("goods-action")),_=C[0],N=C[1];function S(t,e,n,i){return t("div",l()([{class:N()},Object(f["b"])(i,!0)]),[n.default&&n.default()])}var B,$=_(S),I=(n("4b0a"),n("2bb1")),q=(n("7844"),n("5596")),z=(n("bff0"),n("8624")),E=n("7744"),L=n("dfaf"),P=n("f331"),T=Object(d["g"])("collapse-item"),D=T[0],H=T[1],J=["title","icon","right-icon"],A=D({mixins:[P["a"]],props:Object(c["a"])({},L["a"],{name:[String,Number],disabled:Boolean,isLink:{type:Boolean,default:!0}}),data:function(){return{show:null,inited:null}},computed:{items:function(){return this.parent.items},index:function(){return this.items.indexOf(this)},currentName:function(){return Object(d["c"])(this.name)?this.name:this.index},expanded:function(){var t=this;if(!this.parent)return null;var e=this.parent.value;return this.parent.accordion?e===this.currentName:e.some(function(e){return e===t.currentName})}},created:function(){this.findParent("van-collapse"),this.items.push(this),this.show=this.expanded,this.inited=this.expanded},destroyed:function(){this.items.splice(this.index,1)},watch:{expanded:function(t,e){var n=this;null!==e&&(t&&(this.show=!0,this.inited=!0),Object(z["a"])(function(){var e=n.$refs,i=e.content,a=e.wrapper;if(i&&a){var s=i.clientHeight;if(s){var o=s+"px";a.style.height=t?0:o,Object(z["a"])(function(){a.style.height=t?o:0})}else n.onTransitionEnd()}}))}},methods:{onClick:function(){if(!this.disabled){var t=this.parent,e=t.accordion&&this.currentName===t.value?"":this.currentName,n=!this.expanded;this.parent.switch(e,n)}},onTransitionEnd:function(){this.expanded?this.$refs.wrapper.style.height=null:this.show=!1}},render:function(t){var e=this,n=J.reduce(function(t,n){return e.slots(n)&&(t[n]=function(){return e.slots(n)}),t},{});this.slots("value")&&(n.default=function(){return e.slots("value")});var i=t(E["a"],{class:H("title",{disabled:this.disabled,expanded:this.expanded}),on:{click:this.onClick},scopedSlots:n,props:Object(c["a"])({},this.$props)}),a=this.inited&&t("div",{directives:[{name:"show",value:this.show}],ref:"wrapper",class:H("wrapper"),on:{transitionend:this.onTransitionEnd}},[t("div",{ref:"content",class:H("content")},[this.slots()])]);return t("div",{class:[H(),{"van-hairline--top":this.index}]},[i,a])}}),F=Object(d["g"])("collapse"),M=F[0],G=F[1],K=M({props:{accordion:Boolean,value:[String,Number,Array],border:{type:Boolean,default:!0}},data:function(){return{items:[]}},methods:{switch:function(t,e){this.accordion||(t=e?this.value.concat(t):this.value.filter(function(e){return e!==t})),this.$emit("change",t),this.$emit("input",t)}},render:function(t){return t("div",{class:[G(),{"van-hairline--top-bottom":this.border}]},[this.slots()])}}),Q=(n("0653"),n("34e9")),R=(n("c194"),n("c3a6"),n("81e6"),n("9ffb")),U=(n("7f7f"),n("9b7e"),n("a3e2")),V={name:"ItemDetail",components:(B={},Object(o["a"])(B,U["a"].name,U["a"]),Object(o["a"])(B,R["a"].name,R["a"]),Object(o["a"])(B,u["a"].name,u["a"]),Object(o["a"])(B,E["a"].name,E["a"]),Object(o["a"])(B,Q["a"].name,Q["a"]),Object(o["a"])(B,K.name,K),Object(o["a"])(B,A.name,A),Object(o["a"])(B,q["a"].name,q["a"]),Object(o["a"])(B,I["a"].name,I["a"]),Object(o["a"])(B,$.name,$),Object(o["a"])(B,y.name,y),Object(o["a"])(B,v.name,v),B),data:function(){return{goods:{title:"",goodsId:"",price:0,express:"免运费",remain:0,detail:"",thumb:["https://img.yzcdn.cn/public_files/2017/10/24/e5a5a02309a41f9f5def56684808d9ae.jpeg","https://img.yzcdn.cn/public_files/2017/10/24/1791ba14088f9c2be8c610d0a6cc0f93.jpeg"]},stat:!0}},computed:{goodsNum:function(){return this.$store.getters.goodsNum}},methods:{formatPrice:function(){return"¥"+this.goods.price.toFixed(2)},onClickCart:function(){this.$router.push("cart")},sorry:function(){Object(s["a"])("尚在完善中~")},additem:function(t){var e=this.$store.state.goods,n=e.find(function(e){return e.id===t.goodsId},this);if(void 0===n){var i={id:t.goodsId,title:t.title,desc:"",price:t.price,thumb:t.thumb[0],num:1};console.log(t,t.goodsName),this.$store.commit("additem",i),Object(s["a"])("加入购物车成功")}else Object(s["a"])("测试版不支持多次加入")}},created:function(){var t=this.$route.query.goodsId;this.goods.goodsId=t;var e=this.goods;axios.get("/goodsdetail?goodsId="+t).then(function(t){var n=t.data;e.title=n.name,e.price=n.price,e.remain=n.amount,e.thumb=[n.image],e.detail=n.detail}).catch(function(t){e.state=!1,console.log(t.response.status)})},mounted:function(){!1===this.state&&this.$toast.fail("该商品已下架")}},W=V,X=(n("56b9"),n("2877")),Y=Object(X["a"])(W,i,a,!1,null,"5ab5b95a",null);e["default"]=Y.exports},"4cf9":function(t,e,n){},"56b9":function(t,e,n){"use strict";var i=n("a787"),a=n.n(i);a.a},"5fbe":function(t,e,n){},7744:function(t,e,n){"use strict";var i=n("c31d"),a=n("2638"),s=n.n(a),o=n("a142"),c=n("dfaf"),r=n("ba31"),l=n("48f4"),d=n("ad06"),u=Object(o["g"])("cell"),f=u[0],b=u[1];function h(t,e,n,i){var a=e.icon,c=e.size,u=e.title,f=e.label,h=e.value,p=e.isLink,m=e.arrowDirection,g=n.title||Object(o["c"])(u),v=n.default||Object(o["c"])(h),j=n.label||Object(o["c"])(f),O=j&&t("div",{class:[b("label"),e.labelClass]},[n.label?n.label():f]),w=g&&t("div",{class:[b("title"),e.titleClass]},[n.title?n.title():t("span",[u]),O]),x=v&&t("div",{class:[b("value",{alone:!n.title&&!u}),e.valueClass]},[n.default?n.default():t("span",[h])]),k=n.icon?n.icon():a&&t(d["a"],{class:b("left-icon"),attrs:{name:a}}),y=n["right-icon"],C=y?y():p&&t(d["a"],{class:b("right-icon"),attrs:{name:m?"arrow-"+m:"arrow"}}),_=function(t){Object(r["a"])(i,"click",t),Object(l["a"])(i)},N={center:e.center,required:e.required,borderless:!e.border,clickable:p||e.clickable};return c&&(N[c]=c),t("div",s()([{class:b(N),on:{click:_}},Object(r["b"])(i)]),[k,w,x,C,n.extra&&n.extra()])}h.props=Object(i["a"])({},c["a"],l["c"],{clickable:Boolean,arrowDirection:String}),e["a"]=f(h)},a787:function(t,e,n){},bff0:function(t,e,n){},c194:function(t,e,n){"use strict";n("68ef")},dfaf:function(t,e,n){"use strict";n.d(e,"a",function(){return i});var i={icon:String,size:String,center:Boolean,isLink:Boolean,required:Boolean,titleClass:null,valueClass:null,labelClass:null,title:[String,Number],value:[String,Number],label:[String,Number],border:{type:Boolean,default:!0}}}}]);