(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-2d226c99"],{e9c2:function(o,t,a){"use strict";a.r(t);var r=function(){var o=this,t=o.$createElement,a=o._self._c||t;return a("v-container",{staticClass:"mt-6"},[a("v-row",[a("v-col",[a("v-card",{staticClass:"mx-auto"},[a("v-card-text",{staticClass:"py-0"},[a("v-row",[a("v-col",{staticStyle:{"padding-top":"20px"}},[a("span",{staticClass:"page-title primary--text"},[o._v("PRODUTOS")])]),a("v-col",{staticClass:"text-right"},[a("v-btn",{attrs:{dark:"",color:"primary"},on:{click:function(t){return o.abrirDialogoProduto({},!0)}}},[o._v("INSERIR ")])],1)],1)],1)],1)],1)],1),a("v-row",[a("v-col",[a("v-data-table",{attrs:{"show-expand":"",expanded:o.store.produtos,"disable-pagination":"",locale:"pt","hide-default-footer":"",headers:o.headers,items:o.store.produtos,"item-key":"codigo_produto"},scopedSlots:o._u([{key:"item.actions",fn:function(t){var r=t.item;return[a("v-icon",{attrs:{color:"primary"},on:{click:function(t){return o.abrirDialogoProduto(r,!1)}}},[o._v(" mdi-pencil ")]),a("v-icon",{attrs:{color:"primary"},on:{click:function(t){return o.confimarDelecaoProduto(r)}}},[o._v(" mdi-delete ")])]}},{key:"expanded-item",fn:function(t){var r=t.headers,e=t.item;return[a("td",{staticClass:"py-3",attrs:{colspan:r.length}},[a("v-row",[a("v-col"),a("v-col",o._l(e.produto_itens,(function(t){return a("p",{key:t.insumo.codigo_insumo,staticClass:"mb-0"},[o._v(" "+o._s(t.quantidade)+" - "+o._s(t.insumo.descricao)+" (código: "+o._s(t.insumo.codigo_insumo)+") ")])})),0)],1)],1)]}}],null,!0)})],1)],1),a("v-row",{attrs:{justify:"center"}},[a("v-dialog",{attrs:{persistent:"","max-width":"600px"},model:{value:o.produtoDialogo,callback:function(t){o.produtoDialogo=t},expression:"produtoDialogo"}},[a("v-card",[a("v-card-text",[a("v-container",[a("v-row",{staticClass:"mt-4"},[a("v-col",{attrs:{cols:"3"}},[a("v-text-field",{attrs:{label:"Código",placeholder:" ",outlined:"",dense:"","hide-details":"auto"},model:{value:o.produto.codigo_produto,callback:function(t){o.$set(o.produto,"codigo_produto",t)},expression:"produto.codigo_produto"}})],1)],1),a("v-row",{staticClass:"mt-4"},[a("v-col",[a("v-text-field",{attrs:{label:"Descrição",placeholder:" ",outlined:"",dense:"","hide-details":"auto"},model:{value:o.produto.descricao,callback:function(t){o.$set(o.produto,"descricao",t)},expression:"produto.descricao"}})],1)],1)],1)],1),a("v-card-actions",[a("v-spacer"),a("v-btn",{attrs:{color:"primary dark",text:""},on:{click:o.cancelarDialogoProduto}},[o._v("Cancelar")]),a("v-btn",{staticClass:"mr-5",attrs:{disabled:o.desabilitarBotaoSalvar,color:"blue darken-1",text:""},on:{click:o.salvar}},[o._v("Salvar")])],1)],1)],1)],1),a("v-snackbar",{attrs:{top:""},scopedSlots:o._u([{key:"action",fn:function(t){var r=t.attrs;return[a("v-btn",o._b({attrs:{color:"primary",text:""},on:{click:function(t){o.exibirSnackbar=!1}}},"v-btn",r,!1),[o._v(" Fechar ")])]}}]),model:{value:o.exibirSnackbar,callback:function(t){o.exibirSnackbar=t},expression:"exibirSnackbar"}},[o._v(" "+o._s(o.snackbarMensagem)+" ")]),a("v-dialog",{attrs:{persistent:"","max-width":"290"},model:{value:o.confirmaExclusaoDialogo,callback:function(t){o.confirmaExclusaoDialogo=t},expression:"confirmaExclusaoDialogo"}},[a("v-card",[a("v-card-title",{staticClass:"headline"},[o._v("Excluir Produto")]),a("v-card-text",[o._v("Você tem certeza que deseja excluir o produto "+o._s(this.produto.descricao)+" (Código: "+o._s(this.produto.codigo_produto)+")? Esta ação não pode ser desfeita.")]),a("v-card-actions",[a("v-spacer"),a("v-btn",{attrs:{color:"yellow darken-1",text:""},on:{click:function(t){o.confirmaExclusaoDialogo=!1}}},[o._v("Cancelar")]),a("v-btn",{staticClass:"mr-5",attrs:{color:"red darken-1",text:""},on:{click:o.deletarProduto}},[o._v("Excluir")])],1)],1)],1)],1)},e=[],i=(a("4de4"),a("7db0"),a("a9e3"),a("d3b7"),a("96cf"),a("1da1")),c=a("5530"),s=a("07a4"),d={name:"Produto",data:function(){return{store:s["a"],produtos:[],produto:{},produtoDialogo:!1,desabilitarBotaoSalvar:!1,ehNovoProduto:!1,exibirSnackbar:!1,snackbarMensagem:"",confirmaExclusaoDialogo:!1,headers:[{text:"Ingredientes",value:"data-table-expand"},{text:"Codigo",align:"center",value:"codigo_produto",sortable:!0},{text:"Descrição",align:"start",sortable:!0,value:"descricao"},{text:"Ações",align:"center",value:"actions",sortable:!1}]}},methods:{abrirDialogoProduto:function(o,t){this.ehNovoProduto=t,!1===t&&(this.produto=Object(c["a"])({},o)),this.produtoDialogo=!0},cancelarDialogoProduto:function(){this.produto={},this.produtoDialogo=!1},salvar:function(){var o=this;if(this.ehNovoProduto){var t=s["a"].produtos.find((function(t){return t.codigo_produto===o.produto.codigo_produto}));void 0===t?(s["a"].produtos.push(this.produto),s["a"].produtos.sort((function(o,t){return Number(o.codigo_produto)>Number(t.codigo_produto)?1:Number(t.codigo_produto)>Number(o.codigo_produto)?-1:0})),this.persistirAlteracoes()):(this.snackbarMensagem="Já existe um produto com o código ".concat(this.produto.codigo_produto,". Não é possível adicionar dois produtos com o mesmo código."),this.exibirSnackbar=!0)}else{var a=s["a"].produtos.find((function(t){return t.codigo_produto===o.produto.codigo_produto}));a.descricao=this.produto.descricao,a.unidades_pacote=this.produto.unidades_pacote,this.persistirAlteracoes()}},persistirAlteracoes:function(){var o=this;return Object(i["a"])(regeneratorRuntime.mark((function t(){return regeneratorRuntime.wrap((function(t){while(1)switch(t.prev=t.next){case 0:return t.next=2,fetch("".concat("","/api/produtos"),{method:"POST",headers:{Accept:"application/json","Content-Type":"application/json"},body:JSON.stringify(s["a"].produtos)});case 2:o.produto={},o.produtoDialogo=!1;case 4:case"end":return t.stop()}}),t)})))()},confimarDelecaoProduto:function(o){this.produto=o,this.confirmaExclusaoDialogo=!0},deletarProduto:function(){var o=this;s["a"].produtos=s["a"].produtos.filter((function(t){return t.codigo_produto!==o.produto.codigo_produto})),this.produto={},this.confirmaExclusaoDialogo=!1,this.persistirAlteracoes()}}},n=d,l=a("2877"),u=a("6544"),p=a.n(u),v=a("8336"),b=a("b0af"),g=a("99d9"),m=a("62ad"),f=a("a523"),h=a("8fea"),x=a("169a"),_=a("132d"),k=a("0fd9"),D=a("2db4"),C=a("2fa4"),w=a("8654"),y=Object(l["a"])(n,r,e,!1,null,null,null);t["default"]=y.exports;p()(y,{VBtn:v["a"],VCard:b["a"],VCardActions:g["a"],VCardText:g["b"],VCardTitle:g["c"],VCol:m["a"],VContainer:f["a"],VDataTable:h["a"],VDialog:x["a"],VIcon:_["a"],VRow:k["a"],VSnackbar:D["a"],VSpacer:C["a"],VTextField:w["a"]})}}]);
//# sourceMappingURL=chunk-2d226c99.2361ba5f.js.map