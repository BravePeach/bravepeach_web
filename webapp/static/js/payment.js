function submit_payment(gname) {
    swal({
        title: "결제하기",
        text: gname+" 가이드로 선택하시겠습니까?",
        type: "question",
        confirmButtonText: "확인",
        cancelButtonText: "취소",
        confirmButtonColor: "#e64c47",
        cancelButtonColor: "#4a4a4a",
        showCancelButton: true
    }).then(function(){
        swal("payment done");
    });
}