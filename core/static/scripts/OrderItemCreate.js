function CreateItem(btn) {
    var table = document.getElementById("tb_items")
    var mainItem = table.tBodies[table.tBodies.length-1].rows

    mainItem = mainItem[mainItem.length-1] ;

    var cln = mainItem.cloneNode(true);
    var nNextId = parseInt(cln.id.substr(cln.id.length -1,1)) + 1;
    
    cln.id = cln.id.substr(0,cln.id.length-1) + nNextId.toString();
    
    // console.log(table)
    table.tBodies[table.tBodies.length-1].appendChild(cln);
    var td = btn.parentNode
    td.removeChild(btn)
    //var newTable = document.getElementById("tb_items")
    //newTable.appendChild(table)
  }

function RemoveItem(td) {
  //var item = document.getElementById("tb_items")
  var tr  = td.parentNode
  if (tr.length == 1) return

  if (tr.parentNode.lastElementChild == tr) {
    var addBtn = tr.lastElementChild;
    tr.previousElementSibling.appendChild(addBtn);
  }

  tr.parentNode.removeChild(tr)

};


  /*$(document).ready( function(){
    var $unitario = $("#unitario")
    var $quantidade = $("#quantidade")
    var $unit = $unitario.clone()
    $unitario.change(function(event){
      event.preventDefault()
      //var $formData = $(this).serialize()
      //var $endpoint = window.location.href
      alert("quantidade " + $quantidade[0])
      console.log($endpoint)
      $.ajax({
          method: "POST",
          url: $endpoint,
          data: $formData
      })

      

    });

});*/