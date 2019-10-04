function CreateItem() {
    var table = document.getElementById("tb_items")
    var mainItem = table.tBodies[table.tBodies.length-1].rows

    mainItem = mainItem[mainItem.length-1] ;

    var cln = mainItem.cloneNode(true);
    var nNextId = parseInt(cln.id.substr(cln.id.length -1,1)) + 1;
    
    cln.id = cln.id.substr(0,cln.id.length-1) + nNextId.toString();
    var trs = document.getElementsByClassName("tritems")
    for (let x=1; x < trs.length; x++) {
      if (x == trs.length){
        return
      }
      if (document.getElementById(`tritem${x+1}`).style.display === "none") {
        document.getElementById(`tritem${x+1}`).style.display = ''
        return
      }
    }
    

    // cln.getElementsByTagName('input')[0].id = "tipo_prod" + nNextId;
    // cln.getElementsByTagName('input')[0].name = "tipo_prod" + nNextId;
    // cln.getElementsByTagName('input')[1].id = "descricao" + nNextId;
    // cln.getElementsByTagName('input')[1].name = "descricao" + nNextId;
    // cln.getElementsByTagName('input')[2].id = "quantidade" + nNextId;
    // cln.getElementsByTagName('input')[2].name = "quantidade" + nNextId;
    // cln.getElementsByTagName('input')[3].id = "unitario" + nNextId;
    // cln.getElementsByTagName('input')[3].name = "unitario" + nNextId;
    // original.parentNode.appendChild(clone);
    // console.log(table)
    // table.tBodies[table.tBodies.length-1].appendChild(cln);
    // var newTable = document.getElementById("tb_items")
    // newTable.appendChild(table)
  }