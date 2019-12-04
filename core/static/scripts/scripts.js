$(document).ready(function(){

    var searchBtn = $('#search-btn');
    var searchForm = $('#search-form');
    
    searchBtn.on('click', function() {
        searchForm.submit();
    });

    var $maisBtn = $("#maior")
    $maisBtn.click(function(event){
      event.preventDefault()
      $data = $("#table-data")
      $diasSem = $('#last-item')
      console.log($diasSem)
      $.ajax({
          method: "GET",
          url: '/agendamentos/',
          data: {'getdata': 'MAIOR',"dias":$diasSem}
      })

    });


});


/*$(document).ready( function(){
    var $myForm = $(".registerpedidos")
    $myForm.submit(function(event){
      event.preventDefault()
      var $formData = $(this).serialize()
      var $endpoint = window.location.href

      console.log($endpoint)
      $.ajax({
          method: "POST",
          url: $endpoint,
          data: $formData
      })

      

    });

});*/