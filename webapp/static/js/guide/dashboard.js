function inactivate_guide() {
    swal({
        title: '비활성 하기',
        text: "3560명의 여행자가 Stella Oh 가이드님과의 여행을 기다리고 있습니다.\n정말로 비활성화 하시겠습니까?",
        type: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#e64c47',
        cancelButtonColor: '#bbbbbb',
        confirmButtonText: '비활성 하기',
        cancelButtonText: '취소'
    }).then(function () {
        location.href = '../inactivate/';
    });
}
