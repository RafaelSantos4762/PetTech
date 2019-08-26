function confirm_del(){
    if (confirm('Tem certeza que deseja deletar este registro ?')) {
        yourformelement.submit();
    } else {
        return false;
    }

;}