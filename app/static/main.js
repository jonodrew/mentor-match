function handleClick(data_folder) {

  const matching = document.getElementById('matching');

  matching.innerHTML = '<blockquote class="warning-text"><h2 class="heading-sm">Matching has started</h2><p>Your matches are being made. This can take a few minutes. You will be automatically redirected when matching is complete.</p></blockquote>';


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
  fetch(`/tasks/status/${taskID}`, {
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
      const matchButton = document.getElementById('match-button');
      const waitMessage = document.getElementById('wait-message');

      matching.innerHTML = '<blockquote class="warning-text"><h2 class="heading-sm">Matching is complete</h2><p>Mentors and mentees have been matched. You will be redirected in 3 seconds.</p></blockquote>';
      setTimeout(function() {
        window.location.replace(downloadURL)
      }, 3000);
    }
    if (taskStatus === 'SUCCESS' || taskStatus === 'FAILURE') return false;
    setTimeout(function() {
      getStatus(res.task_id);
    }, 1000);

  })
  .catch(err => console.log(err));
}

function redirectToDone() {
    setTimeout(function () {
        window.location.replace("/finished")
    }, 1000);
  // alert("Done")
}
