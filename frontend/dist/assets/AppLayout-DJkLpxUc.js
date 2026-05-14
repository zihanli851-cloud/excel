import{d as S,u as V,c as y,a as e,b as l,w as i,g as o,t as d,m as I,r as n,o as c,F as O,n as A,i as B,p as R,f as j,q as f,s as z,_ as H}from"./index-D8SWB9I1.js";import{c as r}from"./createLucideIcon-8o_oU1rT.js";import{S as N}from"./search-DvEhxumU.js";/**
 * @license lucide-vue-next v0.469.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const D=r("ClipboardListIcon",[["rect",{width:"8",height:"4",x:"8",y:"2",rx:"1",ry:"1",key:"tgr4d6"}],["path",{d:"M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2",key:"116196"}],["path",{d:"M12 11h4",key:"1jrz19"}],["path",{d:"M12 16h4",key:"n85exb"}],["path",{d:"M8 11h.01",key:"1dfujw"}],["path",{d:"M8 16h.01",key:"18s6g9"}]]);/**
 * @license lucide-vue-next v0.469.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const F=r("LogOutIcon",[["path",{d:"M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4",key:"1uf3rs"}],["polyline",{points:"16 17 21 12 16 7",key:"1gabdz"}],["line",{x1:"21",x2:"9",y1:"12",y2:"12",key:"1uyos4"}]]);/**
 * @license lucide-vue-next v0.469.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const P=r("UploadIcon",[["path",{d:"M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4",key:"ih7n3h"}],["polyline",{points:"17 8 12 3 7 8",key:"t8dd8p"}],["line",{x1:"12",x2:"12",y1:"3",y2:"15",key:"widbto"}]]),U={class:"app-shell"},q={class:"app-sidebar"},E={class:"app-main"},T={class:"app-header"},G={class:"app-header-title"},J={class:"app-header-subtitle"},K={class:"app-content"},Q=S({__name:"AppLayout",setup(W){const b=I(),u=j(),a=V(),v=R(()=>[{path:"/search",label:"项目查询",icon:N,adminOnly:!1},{path:"/import",label:"数据导入",icon:P,adminOnly:!0},{path:"/audit/logs",label:"审计日志",icon:D,adminOnly:!0}].filter(t=>!t.adminOnly||a.isAdmin));function k(p){u.push(p)}function x(){a.logout(),u.push("/login")}return(p,t)=>{var h,_,m;const g=n("el-icon"),L=n("el-menu-item"),C=n("el-menu"),w=n("el-button"),M=n("RouterView");return c(),y("div",U,[e("aside",q,[t[0]||(t[0]=e("div",{class:"app-brand"},[e("div",{class:"app-brand-mark"},"PL"),e("div",null,[e("div",{class:"app-brand-title"},"项目清单筛选查询"),e("div",{class:"app-brand-subtitle"},"Project List Console")])],-1)),l(C,{"default-active":o(b).path,class:"app-menu","background-color":"transparent","text-color":"#dbe5f5","active-text-color":"#ffffff",onSelect:k},{default:i(()=>[(c(!0),y(O,null,A(v.value,s=>(c(),f(L,{key:s.path,index:s.path},{default:i(()=>[l(g,null,{default:i(()=>[(c(),f(z(s.icon),{size:16}))]),_:2},1024),e("span",null,d(s.label),1)]),_:2},1032,["index"]))),128))]),_:1},8,["default-active"])]),e("div",E,[e("header",T,[e("div",null,[e("div",G,d(((h=o(a).user)==null?void 0:h.display_name)||((_=o(a).user)==null?void 0:_.username)),1),e("div",J,"角色："+d(((m=o(a).user)==null?void 0:m.role)||"-"),1)]),l(w,{icon:o(F),text:"",onClick:x},{default:i(()=>[...t[1]||(t[1]=[B("退出登录",-1)])]),_:1},8,["icon"])]),e("main",K,[l(M)])])])}}}),$=H(Q,[["__scopeId","data-v-95426d01"]]);export{$ as default};
