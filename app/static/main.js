function handleClick(data_folder) {
  fetch('/tasks', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ data_folder: data_folder }),
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
    if (taskStatus === 'SUCCESS') {
      const downloadURL = res.task_result;
      // Redirect to the download page
      window.location.replace(downloadURL)
      // In the original code, the `download-button` would have been updated with the handleClick function.
      // We'd need the button on the new 'download/etc' page to handle this now.
    }
    if (taskStatus === 'SUCCESS' || taskStatus === 'FAILURE') return false;
    setTimeout(function() {
      getStatus(res.task_id);
    }, 1000);

  })
  .catch(err => console.log(err));
}
