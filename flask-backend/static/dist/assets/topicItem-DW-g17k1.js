import{_ as r,a as s,c as i,e as l,w as d,f as t,t as o,q as p,i as f}from"./index-C7PChkaq.js";const u={class:"cxknum"},_={class:"cxkmiaosu"},I={key:0,class:"cxkjx"},g={__name:"topicItem",props:{topicInfo:Object},setup(e){const a=e,n=()=>{window.location=a.topicInfo.topic_url};return(x,c)=>{const m=f("el-image");return s(),i("div",{class:"topic-item",onClick:n},[l(m,{src:e.topicInfo.avi,class:"imagecxk"},{error:d(()=>c[0]||(c[0]=[t("img",{src:"https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg",style:{width:"100%",height:"100%"}},null,-1)])),_:1},8,["src"]),t("div",null,o(e.topicInfo.name),1),t("div",u,"仓库数:"+o(e.topicInfo.repos_num),1),t("div",_,"描述："+o(e.topicInfo.descript),1),e.topicInfo.is_feature?(s(),i("div",I,"精选")):p("",!0)])}}},k=r(g,[["__scopeId","data-v-fcbeb9d7"]]);export{k as T};