**Managing-Skill**
* from https://wxu26.github.io/writings/claude_for_research.html extract two md files for templates, using these as guiding principles, use these two md directly, modify them to fit the tasks below and keep track of the progress

**central task**
* central target: read through the '/Users/hyw/Desktop/Agent/BDNK/mathematical-derivations.md', '/Users/hyw/Desktop/Agent/BDNK/numerical-implementations.md'; generate mathematica codes and reproduce numerical results in the paper
* re
* first call (plan mode): deploying one agents, converge on the convension for mathematical expression; one agent for mathematical non-step skipping derivations; one agent for numerical implementations; one agent for tests results and test suits/designs
* based on the plan proceed as follows:
* second call (editting mode): deploying one agents, converge on the convension for mathematical expression; one agent for mathematical non-step skipping derivations; one agent for numerical implementations; one agent for tests results and test suits/designs; simultaneously deploy 7 agents for each pdf plots, add the descriptions and implementation/numerical should-be-awared issues in md files
* in editting mode, deploying 11 agents to repeat the task and double check
* final agent check and finalize the reulsts

**FilesAndLinks**
* @NT-Disk.pdf is the original paper
* https://github.com/FoPGSDI/BDNK-NT is the git repo, BDNK-hydro-sim branch

**Commit-Priciples**
* each subagents commit individually
* one commit should be finalized after each stage
* the progress of each subagent should be documented in md files, the final converged convension should be documented in one md files, the stage progress should be documented in one md files according to the original guideline; these should be shown in progress folder
* we should have stage-wise research diaries and final report for human read
