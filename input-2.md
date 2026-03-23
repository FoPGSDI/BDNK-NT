**Managing-Skill**
* from https://wxu26.github.io/writings/claude_for_research.html extract two md files for templates, using these as guiding principles, use these two md directly, modify them to fit the tasks below and keep track of the progress

**central task**
* central target: read through the '/Users/hyw/Desktop/Agent/BDNK/mathematical-derivations.md', '/Users/hyw/Desktop/Agent/BDNK/numerical-implementations.md'; generate mathematica codes and reproduce numerical results in the paper
* 1. first call (plan mode): one agent for mathematical non-step skipping derivations; one agent for numerical implementations; one agent for tests results and test suits/designs
* 2. based on the plan proceed as follows: second call (editting mode): deploying one agents,  one agent for mathematical non-step skipping derivations implementation in mathematica; one agent for numerical implementation
* 3. reproduce the tests
* 4. check for validation, if not the same as the paper figures, document this cycle with a md file including cycle number, commit and push, go back to 1. and this is failed; if same this is succeed

* do not end the loop till 4 suceed

**FilesAndLinks**
* @NT-Disk.pdf is the original paper
* https://github.com/FoPGSDI/BDNK-NT is the git repo, BDNK-hydro-sim branch

**Commit-Priciples**
* each subagents commit individually
* one commit should be finalized after each stage
* the progress of each subagent should be documented in md files, the final converged convension should be documented in one md files, the stage progress should be documented in one md files according to the original guideline; these should be shown in progress folder
* we should have stage-wise research diaries and final report for human read
