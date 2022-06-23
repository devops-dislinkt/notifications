module.exports = {
	branches: ["master", {"name": "dev", "prerelease": true}],
	repositoryUrl: "https://github.com/devops-dislinkt/notifications.git",
	plugins: [
		"@semantic-release/commit-analyzer",
		"@semantic-release/release-notes-generator",
		["@semantic-release/github", {
			assets: [
				{"path": "dist/*.gz", "label": "build"},
						]
		}
		]
	]
}