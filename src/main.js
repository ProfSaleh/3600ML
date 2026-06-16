const app = document.querySelector("#app");

const spectrumStages = [
  {
    label: "Vibe Coding",
    icon: "spark",
    subtitle: "Fast, playful, and fragile",
    promise: "Describe the goal, accept the output, paste errors back, repeat.",
    verification: "Eye test: click around and hope the result holds together.",
    risk: "High token burn, hidden bugs, and spaghetti maintenance debt.",
    habit: "Use it for disposable prototypes and learning experiments.",
  },
  {
    label: "Guided AI Development",
    icon: "guide",
    subtitle: "A human keeps the model pointed",
    promise: "Add clear acceptance criteria, repo examples, and review checkpoints.",
    verification: "Manual review plus focused unit tests for the important paths.",
    risk: "Better than vibes, but still depends heavily on the reviewer.",
    habit: "Move from 'fix this' to 'prove this with tests and explain the tradeoffs.'",
  },
  {
    label: "Agentic Engineering",
    icon: "factory",
    subtitle: "A verifiable software factory",
    promise: "Agents implement inside specs, sandboxes, tools, memory, and guardrails.",
    verification: "Automated tests, CI gates, security checks, and trajectory evaluations.",
    risk: "Higher setup cost, but much lower long-term operating cost.",
    habit: "Design the harness: context, tools, observability, and quality sensors.",
  },
];

const lessons = [
  {
    eyebrow: "Lesson 1",
    title: "Understand the spectrum",
    time: "8 min",
    summary:
      "See why the difference between casual AI coding and production engineering is not whether you use AI; it is how you verify the output.",
    bullets: ["Vibe coding loop", "Agentic verification", "BBQ vs Michelin kitchen analogy"],
  },
  {
    eyebrow: "Lesson 2",
    title: "Engineer context",
    time: "12 min",
    summary:
      "Balance instructions, knowledge, memory, examples, tools, and guardrails without causing context rot.",
    bullets: ["Static vs dynamic context", "Agent skills", "Backpack analogy"],
  },
  {
    eyebrow: "Lesson 3",
    title: "Build the harness",
    time: "14 min",
    summary:
      "Learn why the model is only part of the system and why sandboxes, orchestration, and observability create reliable agents.",
    bullets: ["Model plus harness", "Agent drift", "Quality control sensors"],
  },
  {
    eyebrow: "Lesson 4",
    title: "Work like a modern engineer",
    time: "10 min",
    summary:
      "Practice switching between conductor mode for real-time guidance and orchestrator mode for delegated agent work.",
    bullets: ["The 80% problem", "Human judgment", "Token economy"],
  },
];

const contextPieces = [
  {
    name: "Instructions",
    role: "Define the agent's role, boundaries, and non-negotiable rules.",
    classroom: "Give the agent the assignment rubric before it starts.",
  },
  {
    name: "Knowledge",
    role: "Provide architecture docs, API references, and project constraints.",
    classroom: "Hand over the textbook chapters that matter for this task.",
  },
  {
    name: "Memory",
    role: "Preserve session attempts and longer project state so loops do not repeat.",
    classroom: "Keep a lab notebook of what already worked or failed.",
  },
  {
    name: "Examples",
    role: "Show trusted patterns from the existing codebase.",
    classroom: "Let the agent study solved problems before the exam.",
  },
  {
    name: "Tools",
    role: "Expose the exact CLIs, APIs, files, and sandboxes the agent can use.",
    classroom: "Give access to approved lab equipment only.",
  },
  {
    name: "Guardrails",
    role: "Block risky actions and enforce security, cost, and quality policies.",
    classroom: "Install safety rails before anyone touches the machinery.",
  },
];

const comparisons = [
  ["Primary output", "Lines of code", "The factory that produces code"],
  ["Main bottleneck", "Typing and syntax", "Architecture and verification"],
  ["Testing style", "Does it seem to work?", "Tests, evals, CI gates, and trajectory review"],
  ["Cost pattern", "Low upfront cost, high maintenance cost", "Higher setup cost, lower marginal cost"],
  ["Human role", "Prompt, accept, retry", "Specify, supervise, verify, improve the harness"],
];

const quizQuestions = [
  {
    question: "What most clearly separates vibe coding from agentic engineering?",
    choices: [
      "The brand of AI model being used",
      "Whether outputs are systematically verified",
      "How quickly code appears on screen",
    ],
    answer: 1,
    explanation:
      "Both workflows use AI. The decisive difference is whether the result and the agent's path are verified with reliable checks.",
  },
  {
    question: "Why not paste an entire repository into every prompt?",
    choices: [
      "The model is not allowed to read code",
      "Too much irrelevant context can dilute attention and create context rot",
      "Static context is always more expensive than dynamic context",
    ],
    answer: 1,
    explanation:
      "Context rot happens when irrelevant information overwhelms the signal the model should focus on.",
  },
  {
    question: "In the transcript's factory model, what does the developer design?",
    choices: [
      "Only the final syntax",
      "The harness, checks, tools, and flow that produce reliable code",
      "A single perfect prompt that never changes",
    ],
    answer: 1,
    explanation:
      "The developer moves from bricklayer to factory engineer: designing the system that routes work and verifies quality.",
  },
];

const scriptBeats = [
  {
    time: "0:00",
    title: "AI becomes normal",
    spectrum: "Why this matters",
    narration:
      "Professional developers are already using AI coding tools, and a large share of new code is AI-generated.",
    takeaway: "Students are entering a field where conversation with AI is becoming a core interface.",
  },
  {
    time: "2:03",
    title: "The spectrum appears",
    spectrum: "Vibe coding",
    narration:
      "On the casual end, a developer describes what they want, accepts the code, then pastes errors back and asks the AI to fix it.",
    takeaway: "This is fast for exploration, but the only verification is whether it seems to work.",
  },
  {
    time: "3:00",
    title: "Verification changes everything",
    spectrum: "Agentic engineering",
    narration:
      "The disciplined end uses specs, tests, CI gates, security checks, and evaluations for the AI's reasoning path.",
    takeaway: "Without systematic verification, the workflow is still vibe coding no matter how fancy the prompt sounds.",
  },
  {
    time: "5:01",
    title: "Prompting becomes context engineering",
    spectrum: "Context",
    narration:
      "The new skill is giving the agent the right mix of instructions, knowledge, memory, examples, tools, and guardrails.",
    takeaway: "Students learn to feed the AI a structured diet instead of relying on magic wording.",
  },
  {
    time: "7:31",
    title: "Avoid context rot",
    spectrum: "Dynamic context",
    narration:
      "Pasting everything into the prompt can dilute the signal. Mature agents load detailed context only when it is needed.",
    takeaway: "Good engineers decide what stays always-on and what should be pulled in on demand.",
  },
  {
    time: "11:17",
    title: "Think in factories",
    spectrum: "Harness design",
    narration:
      "The developer's output becomes the system that produces code: sandboxes, orchestration, observability, and quality sensors.",
    takeaway: "The human moves from laying every brick to designing the factory that checks every brick.",
  },
  {
    time: "14:18",
    title: "Choose the operating mode",
    spectrum: "Conductor / Orchestrator",
    narration:
      "Developers move between hands-on conductor mode and async orchestrator mode, depending on the kind of work.",
    takeaway: "The AI handles the routine 80%; humans focus on the strategic 20%.",
  },
  {
    time: "16:45",
    title: "Understand the token economy",
    spectrum: "Cost discipline",
    narration:
      "Vibe coding has low upfront cost but high operational cost. Agentic engineering invests up front to reduce long-term waste.",
    takeaway: "Reliable context and verification reduce retries, token burn, and maintenance debt.",
  },
];

const stageWorkshops = [
  {
    stage: "Vibe Coding",
    badge: "Stage 1",
    learn:
      "Vibe coding is useful when the goal is speed, exploration, or a disposable prototype. The danger is pretending a prototype is production-ready.",
    scenario: "You want a quick campus event planner demo before tomorrow's club fair.",
    aiMove: "Build a simple event planner with cards, filters, and a save button. If it breaks, fix it.",
    example:
      "A student asks the AI for the whole interface, clicks through the demo, and pastes any visible error back into the chat.",
    challenge: "What is the best next move before showing this to real users?",
    choices: [
      {
        text: "Ship it because the buttons worked once.",
        feedback: "That is still pure vibe coding. One manual click path does not prove reliability.",
      },
      {
        text: "Label it a prototype and write down what still needs verification.",
        feedback:
          "Correct. Vibe coding can be valuable as long as students recognize it as exploration, not finished engineering.",
      },
      {
        text: "Paste the whole repository into the next prompt.",
        feedback: "That risks context rot and does not add a real verification plan.",
      },
    ],
    answer: 1,
  },
  {
    stage: "Guided AI Development",
    badge: "Stage 2",
    learn:
      "Guided AI development adds human direction: clearer acceptance criteria, examples from the repo, and focused tests around the riskiest behavior.",
    scenario: "Your planner now needs conflict detection when two study sessions overlap.",
    aiMove:
      "Use the existing event-card pattern. Add overlap detection for same-day sessions. Include tests for boundary times.",
    example:
      "A student supplies expected inputs and outputs, asks for unit tests, and reviews the generated logic before accepting it.",
    challenge: "Which verification habit moves this beyond vibes?",
    choices: [
      {
        text: "Ask the model to explain why it is probably correct.",
        feedback: "Explanations help, but they are not enough without executable checks.",
      },
      {
        text: "Add tests for overlapping, adjacent, and different-day sessions.",
        feedback:
          "Correct. Focused tests turn a generated feature into something students can verify repeatably.",
      },
      {
        text: "Use a bigger model for every retry.",
        feedback: "Model size does not replace acceptance criteria or tests.",
      },
    ],
    answer: 1,
  },
  {
    stage: "Agentic Engineering",
    badge: "Stage 3",
    learn:
      "Agentic engineering treats AI as part of a controlled production system. The harness defines context, tools, sandboxes, guardrails, and quality gates.",
    scenario: "The planner is becoming a course project used by hundreds of students.",
    aiMove:
      "Implement inside a sandbox. Follow the project spec. Run tests, accessibility checks, and security checks before opening a PR.",
    example:
      "A student delegates work to an agent with tool limits, observes logs, checks the trajectory, and only accepts code that passes gates.",
    challenge: "What is the strongest sign this is agentic engineering?",
    choices: [
      {
        text: "The prompt is longer and more detailed.",
        feedback: "A detailed prompt helps, but agentic engineering depends on verification and harness design.",
      },
      {
        text: "The agent used approved tools, passed CI, and produced reviewable evidence.",
        feedback:
          "Correct. The system verifies both the final output and the path the agent took to produce it.",
      },
      {
        text: "The feature was generated faster than a human could type it.",
        feedback: "Speed is expected. Reliability comes from the harness and quality gates.",
      },
    ],
    answer: 1,
  },
];

function iconMarkup(type) {
  const icons = {
    spark: `<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2l1.9 6.1L20 10l-6.1 1.9L12 18l-1.9-6.1L4 10l6.1-1.9L12 2zm6 12l.9 2.6L22 18l-3.1 1.4L18 22l-.9-2.6L14 18l3.1-1.4L18 14z"/></svg>`,
    guide: `<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 5.5A2.5 2.5 0 016.5 3H20v15H7a3 3 0 00-3 3V5.5zm3 0a.5.5 0 000 1h9a.5.5 0 000-1H7zm0 4a.5.5 0 000 1h9a.5.5 0 000-1H7zM6.5 20H20v1H6.5a1 1 0 010-2H20v1H6.5z"/></svg>`,
    factory: `<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 21V9l5 3V9l5 3V5h8v16H3zm12-2h2v-3h-2v3zm-8-1h3v-3H7v3zm9-9h2V7h-2v2zm0 4h2v-2h-2v2z"/></svg>`,
  };

  return icons[type] ?? icons.spark;
}

function lessonCards() {
  return lessons
    .map(
      (lesson, index) => `
        <article class="lesson-card" style="--delay: ${index * 90}ms">
          <div class="lesson-card__meta">
            <span>${lesson.eyebrow}</span>
            <strong>${lesson.time}</strong>
          </div>
          <h3>${lesson.title}</h3>
          <p>${lesson.summary}</p>
          <ul>
            ${lesson.bullets.map((bullet) => `<li>${bullet}</li>`).join("")}
          </ul>
        </article>
      `
    )
    .join("");
}

function contextCards() {
  return contextPieces
    .map(
      (piece, index) => `
        <button class="context-card" type="button" data-context-index="${index}">
          <span>${String(index + 1).padStart(2, "0")}</span>
          <strong>${piece.name}</strong>
          <small>${piece.role}</small>
        </button>
      `
    )
    .join("");
}

function comparisonRows() {
  return comparisons
    .map(
      ([category, vibe, agentic]) => `
        <tr>
          <th scope="row">${category}</th>
          <td>${vibe}</td>
          <td>${agentic}</td>
        </tr>
      `
    )
    .join("");
}

function quizMarkup() {
  return quizQuestions
    .map(
      (item, questionIndex) => `
        <fieldset class="quiz-card" data-question="${questionIndex}">
          <legend>${item.question}</legend>
          <div class="quiz-card__choices">
            ${item.choices
              .map(
                (choice, choiceIndex) => `
                  <label>
                    <input type="radio" name="question-${questionIndex}" value="${choiceIndex}" />
                    <span>${choice}</span>
                  </label>
                `
              )
              .join("")}
          </div>
        </fieldset>
      `
    )
    .join("");
}

function scriptBeatButtons() {
  return scriptBeats
    .map(
      (beat, index) => `
        <button class="beat-button" type="button" data-beat="${index}">
          <span>${beat.time}</span>
          <strong>${beat.title}</strong>
          <small>${beat.spectrum}</small>
        </button>
      `
    )
    .join("");
}

function workshopTabs() {
  return stageWorkshops
    .map(
      (workshop, index) => `
        <button class="workshop-tab" type="button" data-workshop="${index}">
          <span>${workshop.badge}</span>
          <strong>${workshop.stage}</strong>
        </button>
      `
    )
    .join("");
}

function workshopChoices(workshop) {
  return workshop.choices
    .map(
      (choice, index) => `
        <button class="choice-button" type="button" data-choice="${index}">
          ${choice.text}
        </button>
      `
    )
    .join("");
}

app.innerHTML = `
  <header class="site-header">
    <a class="brand" href="#top" aria-label="AgenticU home">
      <span class="brand__mark">AU</span>
      <span>AgenticU</span>
    </a>
    <nav class="site-nav" aria-label="Primary navigation">
      <a href="#journey">Script</a>
      <a href="#spectrum">Spectrum</a>
      <a href="#workshop">Examples</a>
      <a href="#curriculum">Lessons</a>
      <a href="#context">Context</a>
      <a href="#quiz">Quiz</a>
    </nav>
  </header>

  <main id="top">
    <section class="hero section-shell">
      <div class="hero__content">
        <p class="eyebrow">Undergrad learning lab</p>
        <h1>Move from vibe coding to agentic engineering.</h1>
        <p class="hero__lede">
          A friendly, interactive app that teaches students how AI changes software work:
          code generation gets faster, but human judgment moves to context, harness design,
          and verification.
        </p>
        <div class="hero__actions">
          <a class="button button--primary" href="#journey">Start guided journey</a>
          <a class="button button--secondary" href="#workshop">Practice with examples</a>
        </div>
      </div>
      <aside class="hero-card" aria-label="Key benchmark statistics">
        <div class="hero-card__orb"></div>
        <p>Early 2026 benchmark</p>
        <strong>41%</strong>
        <span>of new code is estimated to be entirely AI-generated.</span>
        <div class="stat-row">
          <span>85%</span>
          <small>developers regularly use AI coding tools</small>
        </div>
      </aside>
    </section>

    <section class="section-shell journey" id="journey">
      <div class="section-heading">
        <p class="eyebrow">Script navigator</p>
        <h2>Move through the transcript as a learning path.</h2>
        <p>
          Students can follow the story beat by beat: why AI coding matters, how
          vibe coding works, why verification changes the game, and how the factory
          mindset emerges.
        </p>
      </div>
      <div class="journey-layout">
        <div class="beat-list" aria-label="Transcript learning beats">
          ${scriptBeatButtons()}
        </div>
        <article class="beat-detail" aria-live="polite">
          <div class="beat-detail__topline">
            <span id="beatTime"></span>
            <strong id="beatSpectrum"></strong>
          </div>
          <h3 id="beatTitle"></h3>
          <p id="beatNarration"></p>
          <div class="takeaway-card">
            <span>Student takeaway</span>
            <p id="beatTakeaway"></p>
          </div>
          <div class="journey-controls">
            <button class="button button--secondary" type="button" id="previousBeat">Previous beat</button>
            <button class="button button--primary" type="button" id="nextBeat">Next beat</button>
          </div>
        </article>
      </div>
    </section>

    <section class="section-shell" id="spectrum">
      <div class="section-heading">
        <p class="eyebrow">The spectrum</p>
        <h2>Same AI, different verification discipline.</h2>
        <p>
          Drag the slider or use the stage buttons to see how workflows mature from
          fast experiments into reliable engineering systems.
        </p>
      </div>

      <div class="spectrum-panel">
        <div class="spectrum-slider">
          <label for="spectrumRange">Learning maturity</label>
          <input id="spectrumRange" type="range" min="0" max="2" value="0" step="1" />
          <div class="spectrum-labels" aria-hidden="true">
            <span>Vibes</span>
            <span>Guided</span>
            <span>Agentic</span>
          </div>
        </div>
        <div class="stage-buttons" role="tablist" aria-label="Spectrum stages">
          ${spectrumStages
            .map(
              (stage, index) => `
                <button class="stage-button" type="button" data-stage="${index}" role="tab">
                  ${iconMarkup(stage.icon)}
                  <span>${stage.label}</span>
                </button>
              `
            )
            .join("")}
        </div>
        <article class="stage-detail" aria-live="polite">
          <div class="stage-detail__icon" id="stageIcon"></div>
          <div>
            <p class="eyebrow" id="stageSubtitle"></p>
            <h3 id="stageTitle"></h3>
            <p id="stagePromise"></p>
          </div>
          <dl>
            <div>
              <dt>Verification</dt>
              <dd id="stageVerification"></dd>
            </div>
            <div>
              <dt>Risk profile</dt>
              <dd id="stageRisk"></dd>
            </div>
            <div>
              <dt>Student habit</dt>
              <dd id="stageHabit"></dd>
            </div>
          </dl>
        </article>
      </div>
    </section>

    <section class="section-shell workshop" id="workshop">
      <div class="section-heading">
        <p class="eyebrow">Example workshop</p>
        <h2>Learn each stage, then make the engineering move.</h2>
        <p>
          Each stage uses a student project example. Read the stage, inspect the AI
          move, then choose the best next action. No instructor-provided material is required.
        </p>
      </div>
      <div class="workshop-shell">
        <div class="workshop-progress">
          <span id="workshopProgress">0 of 3 examples completed</span>
          <div class="progress-track"><span id="workshopProgressBar"></span></div>
        </div>
        <div class="workshop-tabs" role="tablist" aria-label="Example workshop stages">
          ${workshopTabs()}
        </div>
        <article class="workshop-panel" aria-live="polite">
          <div class="workshop-panel__header">
            <p class="eyebrow" id="workshopBadge"></p>
            <h3 id="workshopStage"></h3>
            <p id="workshopLearn"></p>
          </div>
          <div class="example-flow">
            <div>
              <span>Scenario</span>
              <p id="workshopScenario"></p>
            </div>
            <div>
              <span>AI move</span>
              <p id="workshopAiMove"></p>
            </div>
            <div>
              <span>What the student sees</span>
              <p id="workshopExample"></p>
            </div>
          </div>
          <div class="challenge-card">
            <h4 id="workshopChallenge"></h4>
            <div class="choice-grid" id="workshopChoices"></div>
            <p class="choice-feedback" id="workshopFeedback"></p>
          </div>
          <div class="journey-controls">
            <button class="button button--secondary" type="button" id="previousWorkshop">Previous stage</button>
            <button class="button button--primary" type="button" id="nextWorkshop">Next stage</button>
          </div>
        </article>
      </div>
    </section>

    <section class="section-shell curriculum" id="curriculum">
      <div class="section-heading">
        <p class="eyebrow">Learning path</p>
        <h2>Four bite-sized modules for modern software judgment.</h2>
        <p>
          Each module uses transcript analogies students can remember: bricklayers,
          Michelin kitchens, hiking backpacks, and factory catwalks.
        </p>
      </div>
      <div class="lesson-grid">
        ${lessonCards()}
      </div>
    </section>

    <section class="section-shell context-lab" id="context">
      <div class="section-heading">
        <p class="eyebrow">Context engineering lab</p>
        <h2>Pack the right context without causing context rot.</h2>
        <p>
          Select a context ingredient to learn what it does and how to explain it
          to a teammate in classroom language.
        </p>
      </div>
      <div class="context-layout">
        <div class="context-grid">
          ${contextCards()}
        </div>
        <article class="context-detail" aria-live="polite">
          <span id="contextNumber">01</span>
          <h3 id="contextTitle"></h3>
          <p id="contextRole"></p>
          <div>
            <strong>Student translation</strong>
            <p id="contextClassroom"></p>
          </div>
        </article>
      </div>
    </section>

    <section class="section-shell split-section" id="factory">
      <div class="factory-card">
        <p class="eyebrow">Factory model</p>
        <h2>The developer designs the system that produces code.</h2>
        <p>
          The transcript frames AI as the robotic arms on the factory floor. Your
          job becomes routing raw materials, setting quality sensors, and deciding
          where human judgment must stay in the loop.
        </p>
        <div class="mode-grid">
          <article>
            <span>Conductor</span>
            <p>Hands-on, real-time guidance for debugging and high-context edits.</p>
          </article>
          <article>
            <span>Orchestrator</span>
            <p>Async delegation for broad goals, sandbox work, tests, and PR review.</p>
          </article>
        </div>
      </div>
      <div class="comparison-card">
        <table>
          <caption>Workflow shift</caption>
          <thead>
            <tr>
              <th scope="col">Dimension</th>
              <th scope="col">Vibe coding</th>
              <th scope="col">Agentic engineering</th>
            </tr>
          </thead>
          <tbody>${comparisonRows()}</tbody>
        </table>
      </div>
    </section>

    <section class="section-shell practice" id="practice">
      <div class="practice-card">
        <p class="eyebrow">Practice studio</p>
        <h2>Rewrite a vibe prompt into an engineering brief.</h2>
        <p class="prompt-label">Vibe prompt</p>
        <blockquote>"Make a study planner app. If it breaks, fix it."</blockquote>
        <div class="brief-grid">
          <label>
            Specification
            <textarea data-brief="spec" placeholder="What must the app do? Who is it for?"></textarea>
          </label>
          <label>
            Verification
            <textarea data-brief="verify" placeholder="What tests, evals, or checks prove it works?"></textarea>
          </label>
          <label>
            Guardrails
            <textarea data-brief="guardrails" placeholder="What should the agent never do?"></textarea>
          </label>
        </div>
        <div class="brief-score">
          <strong id="briefScore">0%</strong>
          <span>engineering brief completeness</span>
        </div>
      </div>
    </section>

    <section class="section-shell quiz-section" id="quiz">
      <div class="section-heading">
        <p class="eyebrow">Knowledge check</p>
        <h2>Can you spot the engineering mindset?</h2>
        <p>Answer three quick questions to reinforce the core ideas.</p>
      </div>
      <form class="quiz-form">
        ${quizMarkup()}
        <button class="button button--primary" type="submit">Check answers</button>
      </form>
      <div class="quiz-result" id="quizResult" role="status" aria-live="polite"></div>
    </section>
  </main>

  <footer class="site-footer">
    <p>Built for students learning to turn AI speed into dependable engineering practice.</p>
    <a href="#top">Back to top</a>
  </footer>
`;

const spectrumRange = document.querySelector("#spectrumRange");
const stageButtons = [...document.querySelectorAll(".stage-button")];
const stageIcon = document.querySelector("#stageIcon");
const stageSubtitle = document.querySelector("#stageSubtitle");
const stageTitle = document.querySelector("#stageTitle");
const stagePromise = document.querySelector("#stagePromise");
const stageVerification = document.querySelector("#stageVerification");
const stageRisk = document.querySelector("#stageRisk");
const stageHabit = document.querySelector("#stageHabit");

const beatButtons = [...document.querySelectorAll(".beat-button")];
const beatTime = document.querySelector("#beatTime");
const beatSpectrum = document.querySelector("#beatSpectrum");
const beatTitle = document.querySelector("#beatTitle");
const beatNarration = document.querySelector("#beatNarration");
const beatTakeaway = document.querySelector("#beatTakeaway");
const previousBeat = document.querySelector("#previousBeat");
const nextBeat = document.querySelector("#nextBeat");

const workshopTabsList = [...document.querySelectorAll(".workshop-tab")];
const workshopProgress = document.querySelector("#workshopProgress");
const workshopProgressBar = document.querySelector("#workshopProgressBar");
const workshopBadge = document.querySelector("#workshopBadge");
const workshopStage = document.querySelector("#workshopStage");
const workshopLearn = document.querySelector("#workshopLearn");
const workshopScenario = document.querySelector("#workshopScenario");
const workshopAiMove = document.querySelector("#workshopAiMove");
const workshopExample = document.querySelector("#workshopExample");
const workshopChallenge = document.querySelector("#workshopChallenge");
const workshopChoicesContainer = document.querySelector("#workshopChoices");
const workshopFeedback = document.querySelector("#workshopFeedback");
const previousWorkshop = document.querySelector("#previousWorkshop");
const nextWorkshop = document.querySelector("#nextWorkshop");

const contextButtons = [...document.querySelectorAll(".context-card")];
const contextNumber = document.querySelector("#contextNumber");
const contextTitle = document.querySelector("#contextTitle");
const contextRole = document.querySelector("#contextRole");
const contextClassroom = document.querySelector("#contextClassroom");

const briefTextareas = [...document.querySelectorAll("[data-brief]")];
const briefScore = document.querySelector("#briefScore");
const quizForm = document.querySelector(".quiz-form");
const quizResult = document.querySelector("#quizResult");

let activeBeatIndex = 0;
let activeWorkshopIndex = 0;
const completedWorkshops = new Set();

function setBeat(index) {
  activeBeatIndex = Math.max(0, Math.min(scriptBeats.length - 1, index));
  const beat = scriptBeats[activeBeatIndex];

  beatTime.textContent = beat.time;
  beatSpectrum.textContent = beat.spectrum;
  beatTitle.textContent = beat.title;
  beatNarration.textContent = beat.narration;
  beatTakeaway.textContent = beat.takeaway;

  beatButtons.forEach((button, buttonIndex) => {
    button.classList.toggle("is-active", buttonIndex === activeBeatIndex);
  });

  previousBeat.disabled = activeBeatIndex === 0;
  nextBeat.disabled = activeBeatIndex === scriptBeats.length - 1;
}

function updateWorkshopProgress() {
  const completed = completedWorkshops.size;
  const total = stageWorkshops.length;
  workshopProgress.textContent = `${completed} of ${total} examples completed`;
  workshopProgressBar.style.width = `${Math.round((completed / total) * 100)}%`;

  workshopTabsList.forEach((button, index) => {
    button.classList.toggle("is-complete", completedWorkshops.has(index));
  });
}

function setWorkshop(index) {
  activeWorkshopIndex = Math.max(0, Math.min(stageWorkshops.length - 1, index));
  const workshop = stageWorkshops[activeWorkshopIndex];

  workshopBadge.textContent = workshop.badge;
  workshopStage.textContent = workshop.stage;
  workshopLearn.textContent = workshop.learn;
  workshopScenario.textContent = workshop.scenario;
  workshopAiMove.textContent = workshop.aiMove;
  workshopExample.textContent = workshop.example;
  workshopChallenge.textContent = workshop.challenge;
  workshopChoicesContainer.innerHTML = workshopChoices(workshop);
  workshopFeedback.textContent = completedWorkshops.has(activeWorkshopIndex)
    ? "Completed. You can still choose another answer to review the feedback."
    : "Choose the best next move.";
  workshopFeedback.className = "choice-feedback";

  workshopTabsList.forEach((button, buttonIndex) => {
    const isSelected = buttonIndex === activeWorkshopIndex;
    button.classList.toggle("is-active", isSelected);
    button.setAttribute("aria-selected", String(isSelected));
  });

  previousWorkshop.disabled = activeWorkshopIndex === 0;
  nextWorkshop.disabled = activeWorkshopIndex === stageWorkshops.length - 1;

  [...workshopChoicesContainer.querySelectorAll(".choice-button")].forEach((button) => {
    button.addEventListener("click", () => {
      chooseWorkshopOption(Number(button.dataset.choice));
    });
  });
}

function chooseWorkshopOption(choiceIndex) {
  const workshop = stageWorkshops[activeWorkshopIndex];
  const isCorrect = choiceIndex === workshop.answer;
  const choice = workshop.choices[choiceIndex];

  if (isCorrect) {
    completedWorkshops.add(activeWorkshopIndex);
  }

  [...workshopChoicesContainer.querySelectorAll(".choice-button")].forEach((button, buttonIndex) => {
    button.classList.toggle("is-correct", buttonIndex === choiceIndex && isCorrect);
    button.classList.toggle("is-incorrect", buttonIndex === choiceIndex && !isCorrect);
  });

  workshopFeedback.textContent = choice.feedback;
  workshopFeedback.classList.toggle("is-correct", isCorrect);
  workshopFeedback.classList.toggle("is-incorrect", !isCorrect);
  updateWorkshopProgress();
}

function setStage(index) {
  const stage = spectrumStages[index];
  spectrumRange.value = String(index);
  stageIcon.innerHTML = iconMarkup(stage.icon);
  stageSubtitle.textContent = stage.subtitle;
  stageTitle.textContent = stage.label;
  stagePromise.textContent = stage.promise;
  stageVerification.textContent = stage.verification;
  stageRisk.textContent = stage.risk;
  stageHabit.textContent = stage.habit;

  stageButtons.forEach((button, buttonIndex) => {
    const isSelected = buttonIndex === index;
    button.classList.toggle("is-active", isSelected);
    button.setAttribute("aria-selected", String(isSelected));
  });
}

function setContext(index) {
  const piece = contextPieces[index];
  contextNumber.textContent = String(index + 1).padStart(2, "0");
  contextTitle.textContent = piece.name;
  contextRole.textContent = piece.role;
  contextClassroom.textContent = piece.classroom;

  contextButtons.forEach((button, buttonIndex) => {
    button.classList.toggle("is-active", buttonIndex === index);
  });
}

function updateBriefScore() {
  const completed = briefTextareas.filter((textarea) => textarea.value.trim().length >= 20).length;
  const score = Math.round((completed / briefTextareas.length) * 100);
  briefScore.textContent = `${score}%`;
}

spectrumRange.addEventListener("input", (event) => {
  setStage(Number(event.target.value));
});

stageButtons.forEach((button) => {
  button.addEventListener("click", () => {
    setStage(Number(button.dataset.stage));
  });
});

beatButtons.forEach((button) => {
  button.addEventListener("click", () => {
    setBeat(Number(button.dataset.beat));
  });
});

previousBeat.addEventListener("click", () => {
  setBeat(activeBeatIndex - 1);
});

nextBeat.addEventListener("click", () => {
  setBeat(activeBeatIndex + 1);
});

workshopTabsList.forEach((button) => {
  button.addEventListener("click", () => {
    setWorkshop(Number(button.dataset.workshop));
  });
});

previousWorkshop.addEventListener("click", () => {
  setWorkshop(activeWorkshopIndex - 1);
});

nextWorkshop.addEventListener("click", () => {
  setWorkshop(activeWorkshopIndex + 1);
});

contextButtons.forEach((button) => {
  button.addEventListener("click", () => {
    setContext(Number(button.dataset.contextIndex));
  });
});

briefTextareas.forEach((textarea) => {
  textarea.addEventListener("input", updateBriefScore);
});

quizForm.addEventListener("submit", (event) => {
  event.preventDefault();

  let correct = 0;
  const explanations = quizQuestions.map((item, index) => {
    const selected = quizForm.querySelector(`input[name="question-${index}"]:checked`);
    const selectedValue = selected ? Number(selected.value) : -1;
    const isCorrect = selectedValue === item.answer;
    if (isCorrect) {
      correct += 1;
    }

    const card = quizForm.querySelector(`[data-question="${index}"]`);
    card.classList.toggle("is-correct", isCorrect);
    card.classList.toggle("is-incorrect", !isCorrect);

    return `<li><strong>Question ${index + 1}:</strong> ${item.explanation}</li>`;
  });

  const message =
    correct === quizQuestions.length
      ? "Excellent. You are thinking like a harness designer."
      : "Review the explanations, then try again.";

  quizResult.innerHTML = `
    <div class="quiz-result__card">
      <strong>${correct}/${quizQuestions.length} correct</strong>
      <p>${message}</p>
      <ul>${explanations.join("")}</ul>
    </div>
  `;
});

setBeat(0);
setStage(0);
setWorkshop(0);
updateWorkshopProgress();
setContext(0);
updateBriefScore();
