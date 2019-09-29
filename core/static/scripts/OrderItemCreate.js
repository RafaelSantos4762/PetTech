function CreateItem() {
    var table = document.getElementById("tb_items")
    var mainItem = table.tBodies[table.tBodies.length-1].rows

    mainItem = mainItem[mainItem.length-1] ;

    var cln = mainItem.cloneNode(true);
    var nNextId = parseInt(cln.id.substr(cln.id.length -1,1)) + 1;
    
    cln.id = cln.id.substr(0,cln.id.length-1) + nNextId.toString();
    table.tBodies[table.tBodies.length-1].appendChild(cln);
  }