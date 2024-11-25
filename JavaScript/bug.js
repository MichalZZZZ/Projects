document.addEventListener('DOMContentLoaded', function () {
	var tooltipTriggerList = [].slice.call(
		document.querySelectorAll('[data-bs-toggle="tooltip"]')
	);
	var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
		return new bootstrap.Tooltip(tooltipTriggerEl);
	});

	// style dla wszystkich elementów
	const bugButton = document.getElementById('show-bugherd'); // przycisk istniejacy
	const stylesBugButton = {
		display: 'flex',
		position: 'fixed',
		height: '50px',
		width: 'auto',
		margin: '10px 0',
		padding: '0',
		right: '0',
		top: '30px',
		border: 'none',
		background: '#0a2d50',
		borderRadius: '12px 0 0 12px',
		maxWidth: '150px',
		zIndex: '1000000',
		fontSize: '13px',
		color: 'white',
		cursor: 'pointer',
		fontSize: '20px',
		transition: 'right 0.3s ease-in-out',
	};
	Object.assign(bugButton.style, stylesBugButton);

	const iconBugButton = document.querySelector('.fa-chevron-left');
	const stylesIconBugButton = {
		marginRight: '5px',
		marginTop: '1px',
	};
	Object.assign(iconBugButton.style, stylesIconBugButton);

	const draggingSpan = document.querySelector('.dragable');
	draggingSpan.setAttribute('title', 'Drag me');
	const styleDragableSpan = {
		cursor: 'grab',
		padding: '10px',
		borderLeft: '2px solid white',
		fontSize: '15px',
		display: 'flex',
		flexDirection: 'column',
	};
	Object.assign(draggingSpan.style, styleDragableSpan);

	const writingBH = document.querySelector('.writing');
	const styleWritingBH = {
		marginRight: '10px',
	};
	Object.assign(writingBH.style, styleWritingBH);

	const openMenu = document.querySelector('.openMenu');
	openMenu.setAttribute('title', 'Open menu');
	const styleOpenMenu = {
		padding: '14px 10px',
		display: 'flex',
		flexDirection: 'row',
	};
	Object.assign(openMenu.style, styleOpenMenu);

	const overlayDiv = document.createElement('div');
	overlayDiv.className = 'overlay';
	const stylesOverlay = {
		position: 'fixed',
		top: '0',
		left: '0',
		width: '100%',
		height: '100%',
		backgroundColor: 'rgba(0, 0, 0, 0.4)',
		display: 'none',
		justifyContent: 'center',
		alignItems: 'center',
		userSelect: 'none',
		webkitUserSelect: 'none',
		mozUserSelect: 'none',
		msUserSelect: 'none',
		zIndex: '1000',
	};
	Object.assign(overlayDiv.style, stylesOverlay);
	document.body.appendChild(overlayDiv);
	const overlay = document.querySelector('.overlay');

	const windowBugherd = document.createElement('div');
	windowBugherd.className = 'window-bugherd';
	const stylesWindowBugherd = {
		flexDirection: 'column',
		justifyContent: 'space-between',
		position: 'fixed',
		right: '-500px',
		top: '10px',
		width: '70px',
		height: 'calc(100% - 20px)',
		border: '1px solid #0a2d50',
		zIndex: '1000',
		backgroundColor: '#0a2d50',
		display: 'flex',
		borderRadius: '15px 0 0 15px',
		textAlign: 'center',
		transition: 'right 0.3s ease-in-out',
	};
	Object.assign(windowBugherd.style, stylesWindowBugherd);

	const screenshotCanvas = document.createElement('canvas');
	screenshotCanvas.id = 'screenshotCanvas';
	const stylesScreenshotCanvas = {
		display: 'none',
		userSelect: 'none',
		webkitUserSelect: 'none',
		mozUserSelect: 'none',
		msUserSelect: 'none',
	};
	Object.assign(screenshotCanvas.style, stylesScreenshotCanvas);

	const newDiv = document.createElement('div');
	newDiv.className = 'new-div';
	const stylesNewDiv = {
		position: 'absolute',
		top: '0',
		left: '0',
		width: '100%',
		height: '100%',
		zIndex: '100',
		backgroundColor: 'white',
		display: 'none',
		zIndex: '10000',
	};
	Object.assign(newDiv.style, stylesNewDiv);

	const stylesVideoContainer = {
		display: 'none',
		position: 'fixed',
		width: '50%',
		height: '50%',
		top: '50%',
		left: '50%',
		transform: 'translate(-50%, -50%)',
		zIndex: '1002',
		flexDirection: 'column',
	};

	const stylesExitVideoContainer = {
		textAlign: 'right',
		cursor: 'pointer',
		fontSize: '20px',
		color: 'white',
		fontWeight: 'bold',
		width: 'auto',
		alignSelf: 'flex-end',
		padding: '5px',
		margin: '3px 0',
		borderRadius: '5px',
		backgroundColor: 'red',
	};

	const stylesBugherdModal = {
		position: 'fixed',
		zIndex: '1001',
		left: '0',
		top: '0',
		width: '100%',
		height: '100%',
		overflow: 'auto',
		backgroundColor: 'rgba(0, 0, 0, 0.4)',
	};

	const stylesBugherdModalContent = {
		backgroundColor: '#fefefe',
		margin: '15% auto',
		padding: '20px',
		border: '1px solid #888',
		width: '80%',
		maxWidth: '600px',
		boxShadow: '0 4px 8px 0 rgba(0,0,0,0.2)',
		borderRadius: '10px',
		fontFamily: 'Arial, sans-serif',
	};

	const stylesCloseButton = {
		color: '#aaa',
		float: 'right',
		fontSize: '28px',
		fontWeight: 'bold',
		cursor: 'pointer',
	};

	const stylesFormOne = {
		display: 'flex',
		flexDirection: 'row',
		gap: '20px',
	};

	const stylesRightForm = {
		display: 'flex',
		flexDirection: 'column',
		gap: '10px',
		width: '50%',
	};

	const stylesLeftForm = {
		width: '50%',
		display: 'flex',
		flexDirection: 'column',
	};

	const styleCreateTaskButtonAndEditContainer = {
		backgroundColor: '#4CAF50',
		color: 'white',
		padding: '10px 20px',
		border: 'none',
		borderRadius: '4px',
		cursor: 'pointer',
		fontSize: '16px',
		marginTop: '34px',
	};

	const stylesStatusSelect = {
		width: '100%',
		padding: '8px',
		marginBottom: '10px',
		border: '1px solid #ccc',
		borderRadius: '4px',
		margin: '5px',
	};

	const stylesLabels = {
		marginBottom: '5px',
		fontWeight: 'bold',
	};

	const stylesDescriptionTextarea = {
		width: '100%',
		padding: '8px',
		marginBottom: '10px',
		border: '1px solid #ccc',
		borderRadius: '4px',
		marginTop: '17px',
		resize: 'none',
		height: '142px',
		maxWidth: '92%',
	};

	const stylesEditScreenButton = {
		backgroundColor: 'blue',
		color: 'white',
		padding: '10px 20px',
		border: 'none',
		borderRadius: '4px',
		cursor: 'pointer',
		fontSize: '16px',
	};

	const stylesMenuVideo = {
		backgroundColor: '#353d47',
		borderRadius: '10px',
		width: 'auto',
		position: 'fixed',
		top: '50px',
		left: 'translate(-50%, -50%)',
		zIndex: '21343434',
		display: 'none',
		flexDirection: 'row',
		justifyContent: 'space-around',
		alignItems: 'flex-start',
		fontFamily: 'Inter, sans-serif',
		fontStyle: 'normal !important',
		fontSize: '16px',
		padding: '3px',
		color: 'white',
	};

	const stylesDragBox = {
		display: 'flex',
		alignItems: 'center',
		cursor: 'grab',
		borderRight: '1px solid #303030',
		padding: '10px',
	};

	const stylesControlBox = {
		display: 'flex',
		padding: '0 10px',
		with: '100%',
	};

	const stylesStopRecording = {
		cursor: 'pointer',
		backgroundColor: '#f44336',
		padding: '5px 10px',
		borderRadius: '4px',
		fontSize: '16px',
		marginLeft: '15px',
		marginTop: '4px',
	};

	const stylesButtons = {
		backgroundColor: '#2f353e',
		borderRadius: '7px 0 0 7px',
		display: 'none',
		flexDirection: 'column',
		justifyContent: 'center',
		alignItems: 'center',
		width: '100%',
		position: 'fixed',
		right: '20px',
		top: '50px',
		width: '50px',
		fontSize: '20px',
		color: 'white',
		zIndex: '999999',
	};

	const stylesIcon = {
		margin: '10px 0',
		cursor: 'pointer',
		padding: '5px',
	};

	const stylesModalContent = {
		position: 'absolute',
		top: '5%',
		left: '40%',
		width: '400px',
		margin: '100px auto',
		borderRadius: '5px',
		boxShadow: '0 2px 8px rgba(0, 0, 0, 0.15)',
		overflow: 'hidden',
		border: '1px solid #e8e8e8',
		display: 'none',
		zIndex: '100111',
	};

	const stylesAntModalClose = {
		position: 'absolute',
		top: '10px',
		right: '10px',
		border: 'none',
		background: 'none',
		fontSize: '16px',
		cursor: 'pointer',
	};

	const stylesModalHeader = {
		padding: '16px 24px',
		background: '#f0f2f5',
		borderBottom: '1px solid #e8e8e8',
	};

	const stylesAntModalTitle = {
		margin: '0',
		fontSize: '16px',
		fontWeight: '500',
	};

	const stylesAntInput = {
		width: '100%',
		padding: '8px 12px',
		borderRadius: '4px',
		border: '1px solid #d9d9d9',
		outline: 'none',
		fontSize: '14px',
	};

	const stylesAntModalFooter = {
		display: 'flex',
		justifyContent: 'flex-end',
		padding: '10px 16px',
		background: '#f0f2f5',
		borderTop: '1px solid #e8e8e8',
	};

	const stylesAntModalBtn = {
		border: 'none',
		borderRadius: '4px',
		padding: '6px 15px',
		fontSize: '14px',
		cursor: 'pointer',
	};

	const stylesAntBtnCancel = {
		background: '#f05f5f5',
		color: 'rgba(0, 0, 0, 0.85)',
	};

	const stylesAntBtnAccept = {
		background: '#1890ff',
		color: '#fff',
	};

	const stylesBH = {
		width: '70px',
		height: '70px',
		display: 'flex',
		alignItems: 'center',
		justifyContent: 'center',
		color: 'white',
		fontSize: '25px',
	};

	const stylesAllButtons = {
		display: 'flex',
		justifyContent: 'center',
		alignItems: 'center',
		backgroundColor: '#0a2d50',
		color: 'white',
		padding: '15px 15px',
		margin: '10px auto',
		cursor: 'pointer',
		border: '2px solid #3f71e0',
		borderRadius: '12px',
		width: '25px',
		height: '25px',
		transition: '0.3s',
	};

	const stylesInputContainer = {
		color: 'white',
		borderRadius: '50%',
		width: '30px',
		backgroundColor: '#2f353e',
		cursor: 'pointer',
	};

	const stylesDragButtonsContainer = {
		padding: '0 10px',
		marginTop: '10px',
		cursor: 'grab',
	};

	const stylesDivSuccess = {
		display: 'flex',
		flexDirection: 'column',
		position: 'fixed',
		top: '40%',
		left: '50%',
		transform: 'translate(-50%, -100%)',
		backgroundColor: 'white',
		padding: '20px',
		borderRadius: '10px',
		boxShadow: '1px 1px 1px 5px rgba(0, 0, 0, 0.5)',
		background: 'linear-gradient(rgb(255 255 255), rgb(224 255 255))',
	};

	const styleDivButton = {
		display: 'flex',
		justifyContent: 'flex-end',
	};

	const stylesHeader = {
		display: 'flex',
		justifyContent: 'space-between',
		fontWeight: 'bold',
		fontSize: '30px',
	};

	const newCanvas = document.createElement('canvas');
	newDiv.appendChild(newCanvas);
	document.body.appendChild(newDiv);
	const newFabricCanvas = new fabric.Canvas(newCanvas);

	let isDragging = false;
	let startY;
	let startTop;
	let wasDragged = false;

	let isBugherdModeEnabled = false;
	let htmlSelector = '';
	let stateCanvas = '';
	let screenOrVideo = 0;

	let mediaRecorder = null;
	let displayStream = null;
	let audioStream = null;

	let oneCancel = false;
	let edit = false;

	let offsetX, offsetY;

	function animation() {
		const keyframes = `
            @keyframes fadeIn {
                0% {
                    opacity: 0;
                }
                100% {
                    opacity: 1;
                }
            }
        `;

		const keyframes2 = `
            @keyframes fadeOut {
                0% {
                    opacity: 1;
                }
                100% {
                    opacity: 0;
                    display: none;
                }
            }
        `;

		const styleElement = document.createElement('style');
		styleElement.type = 'text/css';
		styleElement.appendChild(document.createTextNode(keyframes));
		styleElement.appendChild(document.createTextNode(keyframes2));

		document.head.appendChild(styleElement);
	}

	function applyFadeInAnimation(modal) {
		animation();
		modal.style.animation = 'fadeIn 0.3s forwards';
	}

	function applyFadeOutAnimation(modal) {
		animation();
		modal.style.animation = 'fadeOut 0.3s forwards';
	}

	function startDragging(container, handle) {
		handle.addEventListener('mousedown', function (e) {
			e.preventDefault();

			const offsetX = e.clientX - container.offsetLeft;
			const offsetY = e.clientY - container.offsetTop;

			function moveElement(e) {
				const newX = e.clientX - offsetX;
				const newY = e.clientY - offsetY;

				container.style.left = `${newX}px`;
				container.style.top = `${newY}px`;
			}

			function stopDragging() {
				document.removeEventListener('mousemove', moveElement);
				document.removeEventListener('mouseup', stopDragging);
			}

			document.addEventListener('mousemove', moveElement);
			document.addEventListener('mouseup', stopDragging);
		});
	}

	function hideTooltips() {
		tooltipList.forEach(function (tooltip) {
			tooltip.hide();
		});
	}

	function removeAllObjects() {
		newFabricCanvas.getObjects().forEach((obj) => {
			newFabricCanvas.remove(obj);
		});
	}

	function createWideoContainer() {
		if (document.querySelector('.video-container')) {
			const x = document.querySelector('.video-container');
			document.body.removeChild(x);
		}
		const videoContainer = document.createElement('div');
		videoContainer.className = 'video-container';
		Object.assign(videoContainer.style, stylesVideoContainer);

		const exitButton = document.createElement('span');
		exitButton.className = 'exit-video-container';
		exitButton.textContent = 'X';
		exitButton.setAttribute('title', 'Close');
		Object.assign(exitButton.style, stylesExitVideoContainer);

		exitButton.addEventListener('click', function () {
			videoContainer.style.display = 'none';
			const modal = document.getElementById('bugherd-modal');
			overlay.style.display = 'none';
			modal.style.display = 'block';
		});

		const videoElement = document.createElement('video');
		videoElement.id = 'recording';
		videoElement.controls = true;

		videoContainer.appendChild(exitButton);
		videoContainer.appendChild(videoElement);

		document.body.appendChild(videoContainer);

		screenOrVideo = 1;
	}

	function createModal() {
		if (document.getElementById('bugherd-modal')) {
			const x = document.getElementById('bugherd-modal');
			document.body.removeChild(x);
		}
		const modal = document.createElement('div');
		modal.id = 'bugherd-modal';
		modal.className = 'bugherd-modal';
		Object.assign(modal.style, stylesBugherdModal);

		const modalContent = document.createElement('div');
		modalContent.className = 'bugherd-modal-content';
		Object.assign(modalContent.style, stylesBugherdModalContent);
		modal.appendChild(modalContent);

		const closeButton = document.createElement('span');
		closeButton.className = 'close-button';
		closeButton.innerHTML = '&times;';
		Object.assign(closeButton.style, stylesCloseButton);
		modalContent.appendChild(closeButton);

		const header = document.createElement('h2');
		header.innerText = 'Report an error on the site';
		modalContent.appendChild(header);

		const formContainer = document.createElement('div');
		formContainer.className = 'form-1';
		Object.assign(formContainer.style, stylesFormOne);
		modalContent.appendChild(formContainer);

		const rightForm = document.createElement('div');
		rightForm.className = 'right-form';
		Object.assign(rightForm.style, stylesRightForm);
		formContainer.appendChild(rightForm);

		const assigneeDiv = document.createElement('div');
		rightForm.appendChild(assigneeDiv);
		const assigneeLabel = document.createElement('label');
		assigneeLabel.setAttribute('for', 'assignee');
		assigneeLabel.innerText = 'Assignee:';
		Object.assign(assigneeLabel.style, stylesLabels);
		assigneeDiv.appendChild(assigneeLabel);

		const assignee = document.createElement('div');
		assignee.className = 'assignee';
		assignee.innerText = 'Example login user';
		assignee.style.padding = '5px';
		assigneeDiv.appendChild(assignee);

		const statusDiv = document.createElement('div');
		rightForm.appendChild(statusDiv);
		const statusLabel = document.createElement('label');
		statusLabel.setAttribute('for', 'status');
		statusLabel.innerText = 'Status:';
		Object.assign(statusLabel.style, stylesLabels);
		statusDiv.appendChild(statusLabel);

		const status = document.createElement('div');
		status.className = 'status';
		status.innerText = 'To DO';
		status.style.padding = '5px';
		statusDiv.appendChild(status);

		const priorityDiv = document.createElement('div');
		rightForm.appendChild(priorityDiv);
		const priorityLabel = document.createElement('label');
		priorityLabel.setAttribute('for', 'priority');
		priorityLabel.innerText = 'Priority:';
		Object.assign(priorityLabel.style, stylesLabels);
		priorityDiv.appendChild(priorityLabel);

		const prioritySelect = document.createElement('select');
		prioritySelect.id = 'priority';
		const priorityOption1 = document.createElement('option');
		priorityOption1.innerText = 'Normal';
		const priorityOption2 = document.createElement('option');
		priorityOption2.innerText = 'High';
		const priorityOption3 = document.createElement('option');
		priorityOption3.innerText = 'Low';

		prioritySelect.appendChild(priorityOption1);
		prioritySelect.appendChild(priorityOption2);
		prioritySelect.appendChild(priorityOption3);
		Object.assign(prioritySelect.style, stylesStatusSelect);
		priorityDiv.appendChild(prioritySelect);

		const createTaskButton = document.createElement('button');
		createTaskButton.id = 'create-task-button';
		createTaskButton.className = 'create-task-button';
		createTaskButton.innerText = 'Create task';
		Object.assign(
			createTaskButton.style,
			styleCreateTaskButtonAndEditContainer
		);
		rightForm.appendChild(createTaskButton);

		const leftForm = document.createElement('div');
		leftForm.className = 'left-form';
		Object.assign(leftForm.style, stylesLeftForm);
		formContainer.appendChild(leftForm);

		const descriptionTextarea = document.createElement('textarea');
		descriptionTextarea.id = 'bug-description';
		descriptionTextarea.placeholder = 'Description';
		Object.assign(descriptionTextarea.style, stylesDescriptionTextarea);
		leftForm.appendChild(descriptionTextarea);

		const screenshotLabel = document.createElement('p');
		screenshotLabel.className = 'screenshot-label';
		const editScreenButton = document.createElement('button');
		editScreenButton.id = 'edit-screen';
		if (screenOrVideo === 0) {
			editScreenButton.innerText = 'Edit screenshot';
		} else {
			editScreenButton.innerText = 'Show video';
		}
		leftForm.appendChild(screenshotLabel);

		Object.assign(editScreenButton.style, stylesEditScreenButton);
		leftForm.appendChild(editScreenButton);
		document.body.appendChild(modal);

		editScreenButton.addEventListener('click', () => {
			if (screenOrVideo === 0) {
				modal.style.display = 'none';
				createButtonsContainer();
				const editScreenMenu = document.querySelector('.buttons');
				overlay.style.display = 'block';
				editScreenMenu.style.display = 'flex';
				openInNewDiv(stateCanvas);
				window.scrollTo(0, 0);
				edit = true;
			}
			if (screenOrVideo === 1) {
				const videoContainer = document.querySelector('.video-container');
				modal.style.display = 'none';
				overlay.style.display = 'block';
				applyFadeInAnimation(videoContainer);
				videoContainer.style.display = 'flex';
			}
		});

		createTaskButton.addEventListener('click', () => {
			if (edit === false) {
				sendTask();
			} else {
				stateCanvas = newFabricCanvas.toDataURL('image/png');
				sendTask();
			}
		});

		closeButton.addEventListener('click', () => {
			applyFadeOutAnimation(modal);
			windowBugherd.style.display = 'flex';
		});
	}

	function createMenuVideo() {
		if (document.querySelector('.menu-video')) {
			const x = document.querySelector('.menu-video');
			document.body.removeChild(x);
		}
		const menuVideo = document.createElement('div');
		menuVideo.className = 'menu-video';

		const dragBox = document.createElement('div');
		dragBox.className = 'dragBox';
		dragBox.setAttribute('title', 'Drag me');
		Object.assign(dragBox.style, stylesDragBox);
		dragBox.innerHTML = '<i class="fa-solid fa-up-down-left-right"></i>';
		menuVideo.appendChild(dragBox);

		const controlsBox = document.createElement('div');
		controlsBox.className = 'controlsBox';
		controlsBox.innerHTML =
			'<span class="recording-progress">Recording..</span>';
		Object.assign(controlsBox.style, stylesControlBox);
		menuVideo.appendChild(controlsBox);

		const stopRecordingSpan = document.createElement('span');
		stopRecordingSpan.id = 'stop-recording';
		stopRecordingSpan.setAttribute('title', 'Stop recording');
		const stopRecordingIcon = document.createElement('i');
		stopRecordingIcon.className = 'fa-solid fa-stop';
		stopRecordingSpan.appendChild(stopRecordingIcon);

		Object.assign(stopRecordingSpan.style, stylesStopRecording);
		controlsBox.appendChild(stopRecordingSpan);

		Object.assign(menuVideo.style, stylesMenuVideo);
		document.body.appendChild(menuVideo);

		startDragging(menuVideo, dragBox);
	}

	function createButtonsContainer() {
		if (document.getElementById('buttons')) {
			const x = document.getElementById('buttons');
			document.body.removeChild(x);
		}
		const buttonsContainer = document.createElement('div');
		buttonsContainer.className = 'buttons';
		buttonsContainer.id = 'buttons';

		function createIconSpan(id, iconClasses, tooltipTitle) {
			const span = document.createElement('span');
			span.id = id;
			span.className = 'icon';
			if (tooltipTitle) {
				span.setAttribute('title', tooltipTitle);
			}
			const icon = document.createElement('i');
			icon.className = iconClasses;
			Object.assign(icon.style, stylesIcon);
			span.appendChild(icon);
			return span;
		}

		buttonsContainer.appendChild(
			createIconSpan(
				'cursor-deafult',
				'fa-solid fa-arrow-pointer',
				'Normal cursor'
			)
		);
		buttonsContainer.appendChild(
			createIconSpan('annotation', 'fa-solid fa-plus', 'Add annotation')
		);
		buttonsContainer.appendChild(
			createIconSpan('add-arrow', 'fa-solid fa-arrow-left-long', 'Add arrow')
		);
		buttonsContainer.appendChild(
			createIconSpan('add-square', 'fa-regular fa-square', 'Add square')
		);

		const colorInputContainer = document.createElement('div');
		colorInputContainer.className = 'color-input';
		const colorPicker = document.createElement('input');
		colorPicker.type = 'color';
		colorPicker.id = 'colorPicker';
		colorPicker.value = '#ff0000';
		Object.assign(colorPicker.style, stylesInputContainer);
		colorInputContainer.appendChild(colorPicker);
		buttonsContainer.appendChild(colorInputContainer);

		buttonsContainer.appendChild(
			createIconSpan('download', 'fa-solid fa-download', 'Download')
		);
		buttonsContainer.appendChild(
			createIconSpan(
				'remove-rect',
				'fa-solid fa-trash',
				'Delete selected element'
			)
		);
		buttonsContainer.appendChild(
			createIconSpan('accept-all', 'fa-solid fa-check-double', 'Save')
		);
		buttonsContainer.appendChild(
			createIconSpan('exit-div', 'fa-solid fa-xmark', 'Exit')
		);
		buttonsContainer.appendChild(
			createIconSpan(
				'drag-buttons-container',
				'fa-solid fa-up-down-left-right',
				'Drag me'
			)
		);

		Object.assign(buttonsContainer.style, stylesButtons);
		document.body.appendChild(buttonsContainer);

		const annotationButton = document.getElementById('annotation');
		const addArrowButton = document.getElementById('add-arrow');
		const addSquareButton = document.getElementById('add-square');
		const acceptAllButton = document.getElementById('accept-all');
		const exitButton = document.getElementById('exit-div');
		const removeButton = document.getElementById('remove-rect');
		const downloadButton = document.getElementById('download');
		const normalCursorButton = document.getElementById('cursor-deafult');
		const dragButtonsContainer = document.getElementById(
			'drag-buttons-container'
		);
		Object.assign(dragButtonsContainer.style, stylesDragButtonsContainer);

		const iconDragButtonsContainer = document.querySelector(
			'.fa-up-down-left-right'
		);
		iconDragButtonsContainer.style.cursor = 'grab';

		if (buttonsContainer && dragButtonsContainer) {
			startDragging(buttonsContainer, dragButtonsContainer);
		}

		colorPicker.addEventListener('input', (event) => {
			const color = event.target.value;
			const activeObject = newFabricCanvas.getActiveObject();
			if (activeObject && activeObject.type === 'path') {
				activeObject.set('fill', color);
				activeObject.set('stroke', color);
				newFabricCanvas.renderAll();
			}
			if (activeObject && activeObject.type === 'group') {
				activeObject._objects.forEach((obj) => {
					if (obj.type === 'textbox') {
						obj.set('fill', color);
					}
				});
				newFabricCanvas.renderAll();
			}
			if (activeObject && activeObject.type === 'rect') {
				activeObject.set('stroke', color);
				newFabricCanvas.renderAll();
			}
		});

		annotationButton.addEventListener('click', () => {
			createAntModal();
			const modal = document.querySelector('.ant-modal-content');
			modal.style.display = 'block';
		});

		addArrowButton.addEventListener('click', () => {
			const arrow = makeArrow(100, 100, 200);
			newFabricCanvas.add(arrow);
			newFabricCanvas.setActiveObject(arrow);
			newFabricCanvas.renderAll();
		});

		addSquareButton.addEventListener('click', addSquare);

		exitButton.addEventListener('click', () => {
			newDiv.style.display = 'none';
			overlay.style.display = 'none';
			const modal = document.getElementById('bugherd-modal');
			modal.style.display = 'block';
			buttonsContainer.style.display = 'none';
			if (oneCancel === false) {
				removeAllObjects();
				oneCancel = true;
			}
		});

		removeButton.addEventListener('click', () => {
			const activeObjects = newFabricCanvas.getActiveObjects();
			if (activeObjects.length) {
				activeObjects.forEach((object) => newFabricCanvas.remove(object));
				newFabricCanvas.discardActiveObject();
				newFabricCanvas.requestRenderAll();
			}
		});

		downloadButton.addEventListener('click', () => {
			const dataURL = newFabricCanvas.toDataURL('image/png');
			const link = document.createElement('a');
			link.download = 'screenshot.png';
			link.href = dataURL;
			link.click();
		});

		acceptAllButton.addEventListener('click', () => {
			newDiv.style.display = 'none';
			overlay.style.display = 'none';
			const modal = document.getElementById('bugherd-modal');
			modal.style.display = 'block';
			buttonsContainer.style.display = 'none';
			oneCancel = true;
		});

		normalCursorButton.addEventListener('click', () => {
			newFabricCanvas.defaultCursor = 'default';
		});
	}

	function createAntModal() {
		const modalContent = document.createElement('div');
		modalContent.className = 'ant-modal-content';

		const closeButton = document.createElement('button');
		closeButton.className = 'ant-modal-close';
		Object.assign(closeButton.style, stylesAntModalClose);
		modalContent.appendChild(closeButton);

		const closeSpan = document.createElement('span');
		closeSpan.className = 'ant-modal-close-x';
		closeSpan.innerText = 'X';
		closeSpan.style.fontSize = '18px';
		closeButton.appendChild(closeSpan);

		const modalHeader = document.createElement('div');
		modalHeader.className = 'ant-modal-header';
		Object.assign(modalHeader.style, stylesModalHeader);
		modalContent.appendChild(modalHeader);

		const modalTitle = document.createElement('div');
		modalTitle.className = 'ant-modal-title';
		modalTitle.innerText = 'Wstaw adnotację';
		Object.assign(modalTitle.style, stylesAntModalTitle);
		modalHeader.appendChild(modalTitle);

		const modalBody = document.createElement('div');
		modalBody.className = 'ant-modal-body';
		modalBody.style.padding = '16px 24px;';
		modalContent.appendChild(modalBody);

		const form = document.createElement('form');
		modalBody.appendChild(form);

		const input = document.createElement('input');
		input.type = 'text';
		input.id = 'annotation-text';
		input.className = 'ant-input';
		input.placeholder = 'Wpisz tekst adnotacji';
		Object.assign(input.style, stylesAntInput);
		form.appendChild(input);

		const modalFooter = document.createElement('div');
		modalFooter.className = 'ant-modal-footer';
		Object.assign(modalFooter.style, stylesAntModalFooter);
		modalContent.appendChild(modalFooter);

		const cancelButton = document.createElement('button');
		cancelButton.id = 'cancel-annotation';
		cancelButton.className = 'ant-btn ant-btn-cancel';
		cancelButton.innerText = 'Anuluj';
		Object.assign(cancelButton.style, stylesAntModalBtn);
		Object.assign(cancelButton.style, stylesAntBtnCancel);
		modalFooter.appendChild(cancelButton);

		const addButton = document.createElement('button');
		addButton.id = 'add-annotation';
		addButton.className = 'ant-btn ant-btn-accept';
		addButton.innerText = 'Dodaj';
		Object.assign(addButton.style, stylesAntModalBtn);
		Object.assign(addButton.style, stylesAntBtnAccept);
		modalFooter.appendChild(addButton);

		Object.assign(modalContent.style, stylesModalContent);
		document.body.appendChild(modalContent);

		closeButton.addEventListener('click', () => {
			modalContent.style.display = 'none';
		});

		addButton.addEventListener('click', () => {
			addAnnotationRect(input);
			input.value = '';
			modalContent.style.display = 'none';
		});

		cancelButton.addEventListener('click', () => {
			modalContent.style.display = 'none';
		});
	}

	function handlePageClick(event) {
		if (!isBugherdModeEnabled) return;
		isBugherdModeEnabled = false;
		document.body.style.cursor = 'default';
		document.body.removeEventListener('click', handlePageClick);

		const element = event.target;

		html2canvas(document.body, {
			x: window.scrollX,
			y: window.scrollY,
			width: window.innerWidth,
			height: window.innerHeight,
			useCORS: true,
			allowTaint: true,
		}).then((canvas) => {
			createModal();
			const modal = document.getElementById('bugherd-modal');
			applyFadeInAnimation(modal);
			stateCanvas = canvas.toDataURL('image/png');
		});
		htmlSelector = getElementPath(element);
	}

	function makeScreenshot() {
		document.body.style.cursor = 'default';
		hideTooltips();

		html2canvas(document.body, {
			x: window.scrollX,
			y: window.scrollY,
			width: window.innerWidth,
			height: window.innerHeight,
			useCORS: true,
			allowTaint: true,
		}).then((canvas) => {
			createModal();
			const modal = document.getElementById('bugherd-modal');
			applyFadeInAnimation(modal);
			stateCanvas = canvas.toDataURL('image/png');
		});
		htmlSelector = 'html';
	}

	function getElementPath(element) {
		if (element.id) {
			return `#${element.id}`;
		}
		if (element.tagName.toLowerCase() === 'html') {
			return 'html';
		}
		if (element.tagName.toLowerCase() === 'body') {
			return 'html > body';
		}

		let path = [];
		while (element) {
			let selector = element.tagName.toLowerCase();
			if (element.id) {
				selector += `#${element.id}`;
				path.unshift(selector);
				break;
			} else if (element.className) {
				selector += `.${element.className.split(' ').join('.')}`;
			}

			let sibling = element;
			let nth = 1;
			while ((sibling = sibling.previousElementSibling)) {
				if (sibling.tagName.toLowerCase() == selector) nth++;
			}
			if (nth != 1) selector += `:nth-of-type(${nth})`;

			path.unshift(selector);
			element = element.parentElement;
		}

		return path.join(' > ');
	}

	function createButton(spans, className, title, iconClass) {
		const button = document.createElement('span');
		button.className = className;
		button.setAttribute('title', title);

		const icon = document.createElement('i');
		icon.className = `fa-solid ${iconClass}`;
		icon.style.fontSize = '20px';

		button.appendChild(icon);
		Object.assign(button.style, stylesAllButtons);
		spans.appendChild(button);
		if (button) {
			button.addEventListener('mouseenter', () => {
				button.style.opacity = '0.7';
			});

			button.addEventListener('mouseleave', () => {
				button.style.opacity = '1';
			});
		}
	}

	function createCloseButton(closeSpansDiv) {
		const closeButton = document.createElement('span');
		closeButton.className = 'bugherd-button-close';

		const icon = document.createElement('i');
		icon.className = 'fa-solid fa-chevron-right';

		closeButton.appendChild(icon);
		Object.assign(closeButton.style, stylesAllButtons);
		closeSpansDiv.appendChild(closeButton);

		if (closeButton) {
			closeButton.addEventListener('mouseenter', () => {
				closeButton.style.opacity = '0.7';
			});

			closeButton.addEventListener('mouseleave', () => {
				closeButton.style.opacity = '1';
			});
		}

		closeButton.addEventListener('click', () => {
			toggleMenu();
		});
	}

	async function startRecording() {
		try {
			displayStream = await navigator.mediaDevices.getDisplayMedia({
				video: true,
			});

			if (!displayStream || displayStream.getVideoTracks().length === 0) {
				throw new Error('No video tracks found in display stream.');
			}

			const audioConstraints = { audio: true, video: false };
			const audioPermission = confirm(
				'Do you want to enable microphone for recording audio?'
			);

			if (audioPermission) {
				try {
					audioStream = await navigator.mediaDevices.getUserMedia(
						audioConstraints
					);
				} catch (error) {
					console.error(
						'Microphone access denied or error accessing microphone:',
						error
					);
				}
			}

			const tracks = [...displayStream.getVideoTracks()];
			if (audioStream) {
				tracks.push(...audioStream.getAudioTracks());
			}

			const combinedStream = new MediaStream(tracks);

			if (combinedStream.getTracks().length === 0) {
				throw new Error('Combined stream has no tracks.');
			}

			const menuVideo = document.querySelector('.menu-video');
			menuVideo.style.display = 'flex';
			windowBugherd.style.display = 'none';

			handleSuccess(combinedStream);
		} catch (error) {
			console.error('Error accessing display media:', error);
		}
	}

	function stopRecording() {
		if (mediaRecorder) {
			mediaRecorder.stop();

			if (displayStream) {
				displayStream.getTracks().forEach((track) => track.stop());
			}

			if (audioStream) {
				audioStream.getTracks().forEach((track) => track.stop());
			}

			displayStream = null;
			audioStream = null;

			const menuWideo = document.querySelector('.menu-video');
			menuWideo.style.display = 'none';
			createModal();
			const modal = document.getElementById('bugherd-modal');
			modal.style.display = 'block';
		}
	}

	function handleSuccess(stream) {
		mediaRecorder = new MediaRecorder(stream);
		recordedChunks = [];

		mediaRecorder.ondataavailable = (event) => {
			if (event.data.size > 0) {
				recordedChunks.push(event.data);
			}
		};

		mediaRecorder.onstop = () => {
			const blob = new Blob(recordedChunks, { type: 'video/mp4' });
			const url = URL.createObjectURL(blob);
			const videoElement = document.getElementById('recording');
			videoElement.src = url;
			videoElement.style.display = 'block';
			videoElement.play();

			const reader = new FileReader();
			reader.onloadend = function () {
				const base64data = reader.result;
				window.videoBase64 = base64data;
			};
			reader.readAsDataURL(blob);
		};

		mediaRecorder.start();
	}

	function makeArrow(x1, y1, length) {
		const angle = 0;
		const headLength = 15;
		const x2 = x1 + length;
		const y2 = y1;

		const arrowHead1 = {
			x: x2 - headLength * Math.cos(angle - Math.PI / 6),
			y: y2 - headLength * Math.sin(angle - Math.PI / 6),
		};
		const arrowHead2 = {
			x: x2 - headLength * Math.cos(angle + Math.PI / 6),
			y: y2 - headLength * Math.sin(angle + Math.PI / 6),
		};

		const arrow = new fabric.Path(
			`
            M ${x1} ${y1}
            L ${x2} ${y2}
            M ${arrowHead1.x} ${arrowHead1.y}
            L ${x2} ${y2}
            L ${arrowHead2.x} ${arrowHead2.y}
        `,
			{
				fill: 'yellow',
				stroke: 'yellow',
				strokeWidth: 2,
				selectable: true,
				cornerColor: 'red',
			}
		);

		return arrow;
	}

	function sendTask() {
		const description = document.getElementById('bug-description').value;
		const assignee = document.querySelector('.assignee');
		const priority = document.getElementById('priority').value;
		const status = document.querySelector('.status');

		const task = {
			description,
			assignee: assignee.innerText,
			priority,
			status: status.innerText,
			timestamp: new Date(),
			url: window.location.href,
			selector: htmlSelector,
			userAgent: navigator.userAgent,
			platform: navigator.platform,
			screenResolution: `${window.screen.width}x${window.screen.height}`,
			windowSize: `${window.innerWidth}x${window.innerHeight}`,
			hidden: 0,
		};

		if (screenOrVideo === 0) {
			task.attachment = stateCanvas;
			task.types = 'screenshot';
		} else if (screenOrVideo === 1) {
			task.attachment = window.videoBase64;
			task.types = 'video';
		}

		const modal = document.getElementById('bugherd-modal');

		fetch('http://192.168.8.186/add/data/to/database', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
			},
			mode: 'no-cors',
			body: JSON.stringify(task),
		})
			.then((data) => {
				creaateDivSuccess();
				const success = document.querySelector('.success');
				applyFadeOutAnimation(modal);
				applyFadeInAnimation(success);
			})
			.catch((error) => {
				console.error('Error:', error);
				alert('Wystąpił błąd podczas dodawania zgłoszenia');
				applyFadeOutAnimation(modal);
				windowBugherd.style.display = 'flex';
			});
	}

	function creaateDivSuccess() {
		const divSuccess = document.createElement('div');
		divSuccess.className = 'success';
		Object.assign(divSuccess.style, stylesDivSuccess);
		document.body.appendChild(divSuccess);

		const header = document.createElement('div');
		header.className = 'header';

		const h2 = document.createElement('div');
		h2.className = 'h2';
		h2.innerText = 'The bug has been sent.';
		header.appendChild(h2);

		const iconOk = document.createElement('div');
		iconOk.className = 'iconOK';
		iconOk.innerHTML = '<i class="fa-regular fa-circle-check"></i>';
		iconOk.style.color = 'green';
		header.appendChild(iconOk);

		Object.assign(header.style, stylesHeader);
		divSuccess.appendChild(header);

		const divInfo = document.createElement('div');
		divInfo.className = 'div-info';
		divInfo.style.marginTop = '20px';
		divInfo.innerHTML =
			'<h3>Thank you for your feedback. The bug has been sent to the system.</h3><p>Our team will review it as soon as possible.</p>';

		divSuccess.appendChild(divInfo);

		const divButton = document.createElement('div');
		divButton.className = 'div-button';
		Object.assign(divButton.style, styleDivButton);

		const closeButtonSuccess = document.createElement('button');
		closeButtonSuccess.className = 'close-success';
		Object.assign(
			closeButtonSuccess.style,
			styleCreateTaskButtonAndEditContainer
		);
		closeButtonSuccess.innerHTML = 'Exit';
		closeButtonSuccess.style.marginRight = '10px';
		closeButtonSuccess.style.backgroundColor = 'red';
		divButton.appendChild(closeButtonSuccess);

		const continueButton = document.createElement('button');
		continueButton.className = 'continue';
		continueButton.innerHTML = 'Continue';
		Object.assign(continueButton.style, styleCreateTaskButtonAndEditContainer);
		divButton.appendChild(continueButton);

		divSuccess.appendChild(divButton);

		closeButtonSuccess.addEventListener('click', () => {
			window.location.reload();
		});

		continueButton.addEventListener('click', () => {
			windowBugherd.style.display = 'flex';
			setTimeout(() => {
				document.body.removeChild(divSuccess);
			}, 300);

			applyFadeOutAnimation(divSuccess);
		});
	}

	function openInNewDiv(dataUrl) {
		fabric.Image.fromURL(dataUrl, function (img) {
			newFabricCanvas.setWidth(img.width);
			newFabricCanvas.setHeight(img.height);
			newFabricCanvas.setBackgroundImage(
				img,
				newFabricCanvas.renderAll.bind(newFabricCanvas),
				{
					scaleX: newFabricCanvas.width / img.width,
					scaleY: newFabricCanvas.height / img.height,
				}
			);
			newFabricCanvas.getElement().style.display = 'block';

			newCanvas.style.width = '200';
			newCanvas.style.height = '200';
			newCanvas.style.display = 'block';
		});
		newDiv.style.display = 'block';
	}

	function addSquare() {
		const rect = new fabric.Rect({
			left: 100,
			top: 100,
			width: 100,
			height: 100,
			fill: 'transparent',
			stroke: 'green',
			strokeWidth: 2,
			selectable: true,
			cornerColor: 'red',
		});
		newFabricCanvas.add(rect);
		newFabricCanvas.setActiveObject(rect);
	}

	function addAnnotationRect(input) {
		const tempText = new fabric.Textbox(input.value, {
			fontSize: 20,
			fontFamily: 'Arial',
			width: 1000,
			originX: 'left',
			originY: 'top',
			editable: false,
		});

		const textWidth = tempText.calcTextWidth();
		const rectWidth = textWidth + 20;

		const rect = new fabric.Rect({
			left: 300,
			top: 300,
			width: rectWidth,
			height: 30,
			fill: 'transparent',
			selectable: true,
			hasBorders: true,
			hasControls: true,
			lockRotation: true,
			cornerSize: 8,
			transparentCorners: false,
		});

		const text = new fabric.Textbox(input.value, {
			fontSize: 20,
			fontFamily: 'Arial',
			width: rectWidth - 10,
			originX: 'center',
			originY: 'center',
			editable: true,
		});

		text.set({
			left: rect.left + rect.width / 2,
			top: rect.top + rect.height / 2,
		});

		const group = new fabric.Group([rect, text], {
			left: rect.left,
			top: rect.top,
			selectable: true,
			hasBorders: true,
			hasControls: true,
			lockRotation: true,
			cornerColor: 'red',
		});

		newFabricCanvas.add(group);
		newFabricCanvas.setActiveObject(group);
	}

	function toggleMenu() {
		const menuRight = window.getComputedStyle(windowBugherd).right;
		if (menuRight === '-500px') {
			windowBugherd.style.right = '0px';
			bugButton.style.right = '-500px';
		} else {
			windowBugherd.style.right = '-500px';
			bugButton.style.right = '0px';
		}
	}

	document.body.addEventListener('mouseover', function (event) {
		if (isBugherdModeEnabled) {
			const element = event.target;
			if (element !== document.body && element !== document.documentElement) {
				element.style.outline = '2px solid red';
				element.addEventListener(
					'mouseout',
					function () {
						element.style.outline = '';
					},
					{ once: true }
				);
			}
		}
	});

	document.addEventListener('mousemove', function (event) {
		if (isDragging) {
			const diffY = event.clientY - startY;
			bugButton.style.top = `${startTop + diffY}px`;
			wasDragged = true;
		}
	});

	document.addEventListener('mouseup', function (event) {
		if (isDragging) {
			isDragging = false;
		}
		wasDragged = false;
	});

	draggingSpan.addEventListener('mousedown', function (event) {
		isDragging = true;
		startY = event.clientY;
		startTop = parseInt(window.getComputedStyle(bugButton).top, 10);
	});

	openMenu.addEventListener('click', () => {
		if (!wasDragged) {
			if (!document.body.contains(windowBugherd)) {
				document.body.appendChild(windowBugherd);
			}

			windowBugherd.innerHTML = '';

			const topDiv = document.createElement('div');
			windowBugherd.appendChild(topDiv);

			const bh = document.createElement('div');
			bh.innerHTML = 'BH';
			Object.assign(bh.style, stylesBH);
			topDiv.appendChild(bh);

			const spans = document.createElement('span');
			topDiv.appendChild(spans);

			toggleMenu();

			createButton(spans, 'bugherd-button', 'TAG AN ELEMENT', 'fa-plus');
			const bugherdButton = document.querySelector('.bugherd-button');
			bugherdButton.style.backgroundColor = '#3f71e0';
			bugherdButton.addEventListener('click', () => {
				document.body.appendChild(screenshotCanvas);
				isBugherdModeEnabled = true;
				screenOrVideo = 0;
				document.body.style.cursor = 'crosshair';
				document.body.addEventListener('click', handlePageClick);
				windowBugherd.style.display = 'none';
				removeAllObjects();
				event.stopPropagation();
			});

			createButton(
				spans,
				'bugherd-button-fullscreen',
				'TAG A PAGE',
				'fa-note-sticky'
			);
			const fullScreenBugherdButton = document.querySelector(
				'.bugherd-button-fullscreen'
			);
			fullScreenBugherdButton.addEventListener('click', function () {
				document.body.appendChild(screenshotCanvas);
				hideTooltips();
				screenOrVideo = 0;
				windowBugherd.style.display = 'none';
				setTimeout(function () {
					makeScreenshot();
				}, 100);
				removeAllObjects();
				event.stopPropagation();
			});

			createButton(spans, 'bugherd-button-video', 'VIDEO FEEDBACK', 'fa-video');
			const bugherdButtonVideo = document.querySelector(
				'.bugherd-button-video'
			);
			bugherdButtonVideo.addEventListener('click', () => {
				createWideoContainer();
				createMenuVideo();
				startRecording();
				const recordingProgress = document.querySelector('.recording-progress');
				recordingProgress.style.marginTop = '9px';
				const stop = document.getElementById('stop-recording');
				stop.addEventListener('click', () => {
					stopRecording();
				});
				screenOrVideo = 1;
			});

			const closeSpansDiv = document.createElement('div');
			closeSpansDiv.className = 'close-spans';
			closeSpansDiv.id = 'close-spans';
			windowBugherd.appendChild(closeSpansDiv);
			createCloseButton(closeSpansDiv);
		}
	});
});
