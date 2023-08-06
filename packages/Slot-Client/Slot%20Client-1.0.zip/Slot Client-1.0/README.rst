Slot client





slot_client = SlotClient(URL)

created_project = slot_client.createProject(AUTH_TOKEN, CreateProjectRequest("project-name", "krystek@nsn-intra", "description", 1540));
print "Created project with id " + str(created_project.id) + " and name " + created_project.name

status = slot_client.updateProject(AUTH_TOKEN, UpdateProjectRequest(created_project.id, "new-name", "krystek@nsn-intra", "description", 1540))
print "Project updated with status: " + str(status)

updated_project = slot_client.getProject(AUTH_TOKEN, created_project.id)
print "Updated project with id " + str(updated_project.id) + " and name " + updated_project.name

uploaded_file_response = slot_client.uploadFile(AUTH_TOKEN, UploadFileRequest(updated_project.id, "file-name", "txt"), "file-content")
print "File uploaded to project: " + uploaded_file_response.message

details = slot_client.getProjectDetails(AUTH_TOKEN, updated_project.id)
print "Project details fetched - klondike Id: " + str(details.project.klondike_id)

file_info = slot_client.getProjectFiles(AUTH_TOKEN, updated_project.id)
print "Project file infos fetched - upload date: " + str(file_info.files[0].upload_date)

status = slot_client.deleteProject(AUTH_TOKEN, updated_project.id)
print "Project deleted with status: " + str(status)