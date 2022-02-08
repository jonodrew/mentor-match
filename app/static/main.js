function handleClick(task_id) {
  fetch('/tasks', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ task_id: task_id }),
  })
  .then(response => response.json())
  .then(data => getStatus(data.task_id));
}

function getStatus(taskID) {
  fetch(`/tasks/${taskID}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json'
    },
  })
  .then(response => response.json())
  .then(res => {
    const taskStatus = res.task_status;
    const taskResult = res.task_result;

    const html = `
      <tr>
        <td>${taskID}</td>
        <td>${taskStatus}</td>
        <td>${taskResult}</td>
      </tr>`;
    const newRow = document.getElementById('tasks').insertRow(0);
    newRow.innerHTML = html;



    if (taskStatus === 'SUCCESS') {
      const downloadURL = res.task_result;
        const downloadButton = document.getElementById('download-matches');
      downloadButton.href = downloadURL;
      showDialog('dialog-box');
    }
    if (taskStatus === 'SUCCESS' || taskStatus === 'FAILURE') return false;
    setTimeout(function() {
      getStatus(res.task_id);
    }, 1000);

  })
  .catch(err => console.log(err));
}

function showDialog(x) {
	// show the dialog
	var dialog = document.getElementById(x);
	dialog.showModal();
}

function closeDialog(x) {
	// hide the dialog
	var dialog = document.getElementById(x);
	dialog.close();
}
