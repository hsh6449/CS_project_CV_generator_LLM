document.addEventListener("DOMContentLoaded", function () {
	const userId = document.body.getAttribute("data-user-id");
	let keywords = [];
	let chatHistory = [];
	let currentResumeVersion = "0";

	function selectResume(event, resumeVersion) {
		event.stopPropagation(); // 이벤트 버블링을 막습니다.
		currentResumeVersion = resumeVersion;
		console.log(`Selected Resume Version: ${resumeVersion}`);
		fetch(`/resume/${resumeVersion}/${userId}/`)
			.then((response) => response.text())
			.then((html) => {
				const resumeDisplayContent = document.getElementById(
					"resume-display-content"
				);
				if (resumeDisplayContent) {
					resumeDisplayContent.innerHTML = html;
				} else {
					console.error("Element #resume-display-content not found.");
				}
				return fetch(`/api/resume-keywords/${resumeVersion}/${userId}/`);
			})
			.then((response) => {
				if (!response.ok) {
					throw new Error("Failed to fetch keywords");
				}
				return response.json();
			})
			.then((data) => {
				const keywordsContainer = document.getElementById("keywords");
				if (keywordsContainer) {
					keywordsContainer.innerHTML = "";
					if (!data.keywords || data.keywords.length === 0) {
						const noKeywordsElement = document.createElement("div");
						noKeywordsElement.textContent = "No keywords found.";
						keywordsContainer.appendChild(noKeywordsElement);
					} else {
						data.keywords.forEach((keyword) => {
							const keywordElement = document.createElement("div");
							keywordElement.classList.add("keyword");
							keywordElement.textContent = keyword.keyword;
							keywordsContainer.appendChild(keywordElement);
						});
					}
				} else {
					console.error("Element #keywords not found.");
				}
			})
			.catch((error) => {
				console.error("Error loading the resume:", error);
				const keywordsContainer = document.getElementById("keywords");
				if (keywordsContainer) {
					keywordsContainer.innerHTML = "";
					const noKeywordsElement = document.createElement("div");
					noKeywordsElement.textContent = "No keywords found.";
					keywordsContainer.appendChild(noKeywordsElement);
				}
			});
	}

	// function downloadPDF() {
	// 	const element = document.getElementById("resume-display-content");

	// 	html2canvas(element).then((canvas) => {
	// 		const imgData = canvas.toDataURL("image/png");
	// 		const pdf = new jsPDF({
	// 			orientation: "portrait",
	// 			unit: "pt",
	// 			format: "a4",
	// 		});
	// 		const imgProps = pdf.getImageProperties(imgData);
	// 		const pdfWidth = pdf.internal.pageSize.getWidth();
	// 		const pdfHeight = (imgProps.height * pdfWidth) / imgProps.width;
	// 		pdf.addImage(imgData, "PNG", 0, 0, pdfWidth, pdfHeight);
	// 		pdf.save("resume.pdf");
	// 	});
	// }

	function sendMessage() {
		const chatInput = document.getElementById("chat-input");
		const messages = document.getElementById("messages");
		const message = chatInput.value;

		if (message.trim() !== "") {
			const placeholderMessage = document.getElementById("placeholder-message");
			if (placeholderMessage) {
				placeholderMessage.remove();
			}

			const userMessage = document.createElement("div");
			userMessage.classList.add("message", "user-message");
			userMessage.innerText = `you: ${message}`;
			messages.appendChild(userMessage);

			chatHistory.push(`User: ${message}`);

			const csrftoken = getCookie("csrftoken");
			const payload = JSON.stringify({
				user_id: userId,
				prompt: message,
				keywords: keywords,
			});

			fetch("/api/update-cv/", {
				method: "POST",
				headers: {
					"Content-Type": "application/json",
					"X-CSRFToken": csrftoken,
				},
				body: payload,
			})
				.then((response) => {
					if (!response.ok) {
						return response.text().then((errorText) => {
							console.error("Error response text:", errorText);
							throw new Error("Network response was not ok");
						});
					}
					return response.json();
				})
				.then((data) => {
					const chatText = data.chat;
					const cvText = data.cv_text;

					if (chatText) {
						const botMessage = document.createElement("div");
						botMessage.classList.add("message", "bot-message");
						botMessage.innerText = `이력서: ${chatText}`;
						messages.appendChild(botMessage);

						chatHistory.push(`LLM: ${chatText}`);
					}

					if (cvText) {
						const cvContainer = document.getElementById(
							"resume-display-content"
						);
						if (cvContainer) {
							cvContainer.innerHTML = cvText;
						} else {
							console.error("CV container not found");
						}

						// 새로운 이력서 버전을 목록에 추가
						const resumeList = document.getElementById("resume-list");
						if (resumeList) {
							const newVersionItem = document.createElement("li");
							newVersionItem.classList.add("list-group-item");
							newVersionItem.dataset.resumeVersion = currentResumeVersion;
							newVersionItem.textContent = `버전 ${currentResumeVersion}`;
							newVersionItem.addEventListener("click", function (event) {
								selectResume(event, currentResumeVersion);
							});
							resumeList.appendChild(newVersionItem);
						}
					}
				})
				.catch((error) => {
					console.error("Error:", error);
					const errorMessage = document.createElement("div");
					errorMessage.classList.add("message", "error-message");
					errorMessage.innerText = `Error: ${error.message}`;
					messages.appendChild(errorMessage);
				});

			chatInput.value = "";
		}
	}

	function getCookie(name) {
		let cookieValue = null;
		if (document.cookie && document.cookie !== "") {
			const cookies = document.cookie.split(";");
			for (let i = 0; i < cookies.length; i++) {
				const cookie = cookies[i].trim();
				if (cookie.substring(0, name.length + 1) === name + "=") {
					cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
					break;
				}
			}
		}
		return cookieValue;
	}

	function openModal() {
		const modal = document.getElementById("analyze-modal");
		modal.style.display = "block";
	}

	function closeModal() {
		const modal = document.getElementById("analyze-modal");
		modal.style.display = "none";
	}

	function analyzeJobDescription() {
		const jobDescription = document.getElementById("job-description").value;

		if (jobDescription.trim() !== "") {
			const csrftoken = getCookie("csrftoken");
			const payload = JSON.stringify({
				job_description: jobDescription,
				user_id: userId,
				resume_version: currentResumeVersion,
			});

			fetch("/api/analyze-job-description/", {
				method: "POST",
				headers: {
					"Content-Type": "application/json",
					"X-CSRFToken": csrftoken,
				},
				body: payload,
			})
				.then((response) => {
					if (!response.ok) {
						return response.text().then((errorText) => {
							console.error("Error response text:", errorText);
							throw new Error("Network response was not ok");
						});
					}
					return response.json();
				})
				.then((data) => {
					keywords = data.keywords;
					currentResumeVersion = data.resume_version;
					displayKeywords(keywords);
					closeModal();
					console.log("Extracted keywords:", keywords);
				})
				.catch((error) => {
					console.error("Error:", error);
				});
		}
	}

	function displayKeywords(keywords) {
		const keywordsContainer = document.getElementById("keywords");
		if (keywordsContainer) {
			keywordsContainer.innerHTML = "";
			if (!keywords || keywords.length === 0) {
				const noKeywordsElement = document.createElement("div");
				noKeywordsElement.textContent = "No keywords found.";
				keywordsContainer.appendChild(noKeywordsElement);
			} else {
				keywords.forEach((keyword) => {
					const keywordElement = document.createElement("div");
					keywordElement.classList.add("keyword");
					keywordElement.innerText = keyword;
					keywordsContainer.appendChild(keywordElement);
				});
			}
		} else {
			console.error("Element #keywords not found.");
		}
	}

	// document
	// 	.getElementById("download-button")
	// 	.addEventListener("click", downloadPDF);
	document.getElementById("send-button").addEventListener("click", sendMessage);
	document
		.getElementById("analyze-button")
		.addEventListener("click", openModal);
	document
		.getElementById("submit-job-description")
		.addEventListener("click", analyzeJobDescription);
	document.querySelector(".close").addEventListener("click", closeModal);

	window.onclick = function (event) {
		const modal = document.getElementById("analyze-modal");
		if (event.target === modal) {
			closeModal();
		}
	};

	// Add keydown event listener for the chat input
	document
		.getElementById("chat-input")
		.addEventListener("keydown", function (event) {
			if (event.key === "Enter") {
				event.preventDefault();
				sendMessage();
			}
		});

	// Add click event listeners for the resume list items after DOM is fully loaded
	document.querySelectorAll(".list-group-item").forEach((item) => {
		item.addEventListener("click", function (event) {
			const resumeVersion = this.getAttribute("data-resume-version");
			selectResume(event, resumeVersion);
		});
	});

	// Load initial resume
	selectResume(new Event("DOMContentLoaded"), "0");
});
