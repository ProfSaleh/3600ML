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
    tag: "Core idea",
    summary:
      "See why the difference between casual AI coding and production engineering is not whether you use AI; it is how you verify the output.",
    bullets: ["Vibe coding loop", "Agentic verification", "BBQ vs Michelin kitchen analogy"],
  },
  {
    eyebrow: "Lesson 2",
    title: "Engineer context",
    tag: "Context",
    summary:
      "Balance instructions, knowledge, memory, examples, tools, and guardrails without causing context rot.",
    bullets: ["Static vs dynamic context", "Agent skills", "Backpack analogy"],
  },
  {
    eyebrow: "Lesson 3",
    title: "Build the harness",
    tag: "Harness",
    summary:
      "Learn why the model is only part of the system and why sandboxes, orchestration, and observability create reliable agents.",
    bullets: ["Model plus harness", "Agent drift", "Quality control sensors"],
  },
  {
    eyebrow: "Lesson 4",
    title: "Work like a modern engineer",
    tag: "Workflow",
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
    chapter: "Step 01",
    title: "AI coding is now the default environment",
    spectrum: "Why this matters",
    narration:
      "The transcript opens with a major shift: most professional developers regularly use AI coding tools, and a large share of new code is AI-generated. Students are not preparing for a future where AI might matter; they are entering a field where AI already shapes daily software work.",
    takeaway:
      "The student mindset changes from 'Will I use AI?' to 'How do I use AI responsibly and skillfully?'",
  },
  {
    chapter: "Step 02",
    title: "Typing syntax is no longer the main bottleneck",
    spectrum: "Intent as interface",
    narration:
      "The transcript compares old programming to laying every brick by hand. With AI, the developer can describe the house, sketch the layout, and guide a fast construction crew. The conversation becomes part of the interface with the machine.",
    takeaway:
      "Students still need technical judgment, but their value moves from typing every line to deciding what should be built and how it should be checked.",
  },
  {
    chapter: "Step 03",
    title: "The spectrum begins with vibe coding",
    spectrum: "Vibe coding",
    narration:
      "Vibe coding is the casual workflow: describe what you want, accept what the AI gives you, paste errors back, and say 'fix this.' It is fast, playful, and useful for discovery, but it depends on trial and error.",
    takeaway:
      "Vibe coding is not bad for exploration. It becomes risky when students mistake a quick demo for reliable software.",
  },
  {
    chapter: "Step 04",
    title: "Agentic engineering is the disciplined end",
    spectrum: "Agentic engineering",
    narration:
      "At the other end of the spectrum, the AI still writes code, but it works inside formal specifications, automated tests, CI gates, security checks, and evaluation routines. The process is designed to produce evidence, not just output.",
    takeaway:
      "The difference is not whether AI is used. The difference is whether AI output is systematically verified.",
  },
  {
    chapter: "Step 05",
    title: "Verification is the turning point",
    spectrum: "From vibes to proof",
    narration:
      "The transcript makes this point directly: without systematic verification, you are still vibe coding no matter how impressive the initial prompt is. Agentic engineering checks deterministic code with tests and AI reasoning with evaluations.",
    takeaway:
      "Students should ask, 'What would prove this works?' before asking, 'Can the AI build this faster?'",
  },
  {
    chapter: "Step 06",
    title: "Remember the BBQ and Michelin kitchen",
    spectrum: "Quality analogy",
    narration:
      "Vibe coding is like a backyard BBQ: casual, forgiving, and okay for low-risk experiments. Agentic engineering is like a Michelin kitchen: measured ingredients, strict protocols, and quality checks before anything reaches a customer.",
    takeaway:
      "The level of verification should match the level of risk and responsibility.",
  },
  {
    chapter: "Step 07",
    title: "Prompt engineering gives way to context engineering",
    spectrum: "Context engineering",
    narration:
      "The transcript argues that clever wording is no longer the core skill. The modern skill is context engineering: giving the AI structured information about the task, codebase, architecture, and constraints.",
    takeaway:
      "Students learn to prepare the agent's environment, not just write a clever prompt.",
  },
  {
    chapter: "Step 08",
    title: "Balance the six context ingredients",
    spectrum: "Six-part context",
    narration:
      "The agent needs instructions, knowledge, memory, examples, tools, and guardrails. Instructions define boundaries. Knowledge supplies docs. Memory prevents repeated loops. Examples show house style. Tools enable action. Guardrails block unsafe moves.",
    takeaway:
      "Good AI work is structured. Each ingredient gives the model a different kind of support.",
  },
  {
    chapter: "Step 09",
    title: "Avoid context rot",
    spectrum: "Signal vs noise",
    narration:
      "More context is not always better. If a student dumps an entire repository into the prompt, the model may lose focus, follow irrelevant files, or forget the main instruction. The transcript calls this context rot.",
    takeaway:
      "Students should provide the right context, not the most context.",
  },
  {
    chapter: "Step 10",
    title: "Use dynamic context like a hiking map",
    spectrum: "Agent skills",
    narration:
      "Static context is like survival gear you always carry. Dynamic context is like a specific trail map you pull out only when needed. Agent skills load relevant schemas, tools, and docs on demand, then put that context away.",
    takeaway:
      "Students learn to keep core rules visible while loading specialized details only for the current task.",
  },
  {
    chapter: "Step 11",
    title: "The software life cycle shifts",
    spectrum: "Modern SDLC",
    narration:
      "When implementation gets faster, the bottlenecks move. Requirements become a live conversation with prototypes. Testing becomes more than checking whether code compiles. Architecture and verification become the high-value human work.",
    takeaway:
      "Students should see AI as changing the entire workflow, not just speeding up coding.",
  },
  {
    chapter: "Step 12",
    title: "Evaluate the trajectory, not only the result",
    spectrum: "Trajectory evaluation",
    narration:
      "The transcript warns that a piece of code can appear to work while taking an unsafe path. Trajectory evaluation asks: Did the agent use approved tools? Did it check permissions? Did it bypass a security step?",
    takeaway:
      "Students should grade the agent's work process, not just the final answer.",
  },
  {
    chapter: "Step 13",
    title: "AI can help with legacy systems",
    spectrum: "Maintenance",
    narration:
      "The transcript explains that AI agents can map and refactor old systems that teams were previously afraid to touch. This makes maintenance and modernization part of the agentic engineering story.",
    takeaway:
      "Students should understand that AI is useful beyond greenfield projects; it can help reason through existing code.",
  },
  {
    chapter: "Step 14",
    title: "Think in factories, not isolated code",
    spectrum: "Factory model",
    narration:
      "The developer's primary output becomes the factory that produces code. Instead of hand-tightening every bolt, the developer designs robotic arms, routes materials, and places quality sensors.",
    takeaway:
      "The new craft is building the system that repeatedly produces reliable software.",
  },
  {
    chapter: "Step 15",
    title: "An agent is the model plus the harness",
    spectrum: "Harness design",
    narration:
      "The transcript emphasizes that the model alone is not the whole agent. The harness supplies sandboxes, orchestration, observability, logs, execution traces, cost metering, and controls that prevent drift.",
    takeaway:
      "When an agent fails, students should inspect the harness and context before simply blaming the model.",
  },
  {
    chapter: "Step 16",
    title: "Choose conductor or orchestrator mode",
    spectrum: "Operating modes",
    narration:
      "In conductor mode, the developer guides the AI in real time inside the editor. In orchestrator mode, the developer delegates a larger goal to an agent working asynchronously in a sandbox and reviews the result.",
    takeaway:
      "Students learn to choose the right collaboration style for the task.",
  },
  {
    chapter: "Step 17",
    title: "Understand the 80% problem",
    spectrum: "Human judgment",
    narration:
      "AI can often generate the routine 80% of a feature quickly. The hard 20% remains edge cases, business logic, architecture, and system integration. Human expertise concentrates where judgment matters most.",
    takeaway:
      "Students should not blindly accept output; they should spend saved time on review, strategy, and verification.",
  },
  {
    chapter: "Step 18",
    title: "Manage the token economy",
    spectrum: "Cost discipline",
    narration:
      "Vibe coding has low upfront cost but high operational cost: retries, huge prompts, hallucinations, and maintenance debt. Agentic engineering has higher upfront setup but lower long-term cost because the factory gets more work right earlier.",
    takeaway:
      "Students learn that better engineering lowers both technical debt and AI usage waste.",
  },
  {
    chapter: "Step 19",
    title: "Route models intelligently",
    spectrum: "Model routing",
    narration:
      "The transcript describes routing complex reasoning to stronger models and simple tasks to cheaper, faster models. The harness becomes a traffic cop that protects quality while reducing cost.",
    takeaway:
      "Not every task needs the most expensive model. Mature systems match model power to task difficulty.",
  },
  {
    chapter: "Step 20",
    title: "The mentorship gap becomes the big question",
    spectrum: "Junior developer growth",
    narration:
      "The transcript ends with a challenge: if AI lays many of the bricks, how do junior developers learn architectural judgment? The answer starts with guided practice, examples, verification habits, and reflection.",
    takeaway:
      "This app exists to help students practice the judgment that future engineers will need most.",
  },
];

const stageWorkshops = [
  {
    stage: "Vibe Coding",
    badge: "Example 1",
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
    stage: "Vibe Coding",
    badge: "Example 2",
    learn:
      "A vibe loop often feels productive because the screen changes quickly. Students need to notice when they are only reacting to visible errors.",
    scenario: "A classmate asks for a flashcard app that generates cards from lecture notes.",
    aiMove: "Make the app look good and generate flashcards. Here is the error I got. Fix it.",
    example:
      "The app works for one short paragraph, but no one checks long notes, duplicate cards, missing answers, or whether private notes are stored safely.",
    challenge: "Which move keeps this in a safe learning zone?",
    choices: [
      {
        text: "Call it an experiment and list the unknowns before adding real lecture notes.",
        feedback:
          "Correct. The student can keep exploring while clearly naming the missing checks and privacy questions.",
      },
      {
        text: "Ask the AI to add every possible feature next.",
        feedback: "More features increase complexity before the student understands whether the core behavior is safe.",
      },
      {
        text: "Ignore edge cases because the first paragraph worked.",
        feedback: "That is the classic eye test. It does not verify realistic student use.",
      },
    ],
    answer: 0,
  },
  {
    stage: "Vibe Coding",
    badge: "Example 3",
    learn:
      "Vibe coding can burn tokens quickly because every failure becomes another vague retry. Better prompts help, but verification is the real upgrade.",
    scenario: "You ask AI to create a grade calculator with weighted assignments.",
    aiMove: "This total is wrong. Fix it. Now the dropdown broke. Fix that too.",
    example:
      "After several retries, the UI looks better but the math is still wrong when weights do not add to 100%.",
    challenge: "What should the student do next?",
    choices: [
      {
        text: "Keep retrying until the displayed number looks reasonable.",
        feedback: "That keeps the student in trial-and-error mode.",
      },
      {
        text: "Write three sample grading cases with expected totals.",
        feedback:
          "Correct. Even a small set of expected examples starts moving the work toward guided verification.",
      },
      {
        text: "Switch colors so the calculator feels more finished.",
        feedback: "Visual polish does not address the reliability problem.",
      },
    ],
    answer: 1,
  },
  {
    stage: "Guided AI Development",
    badge: "Example 4",
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
    stage: "Guided AI Development",
    badge: "Example 5",
    learn:
      "Context engineering starts when the student gives the model relevant rules, examples, and constraints instead of a blank request.",
    scenario: "A team project needs a discussion-board moderation helper.",
    aiMove:
      "Follow our existing comment-card style. Flag harassment, threats, and spam. Do not auto-delete posts. Return a confidence score and reason.",
    example:
      "The student provides three sample posts, a UI component example, and a rule that human review is required before action.",
    challenge: "Which context ingredient is most obvious here?",
    choices: [
      {
        text: "Guardrails, because the AI is blocked from auto-deleting posts.",
        feedback:
          "Correct. The student is defining a safety boundary around what the AI may do.",
      },
      {
        text: "Context rot, because the prompt contains more than one sentence.",
        feedback: "Context rot is about irrelevant overload, not useful task constraints.",
      },
      {
        text: "Model routing, because the UI uses cards.",
        feedback: "Model routing is about choosing different models for different task types.",
      },
    ],
    answer: 0,
  },
  {
    stage: "Guided AI Development",
    badge: "Example 6",
    learn:
      "Guided work teaches students to ask for evidence and compare output against known project patterns.",
    scenario: "You need an accessibility improvement for a course-registration form.",
    aiMove:
      "Update labels, keyboard focus, and error messages. Match the current form components. Include a checklist of accessibility checks.",
    example:
      "The AI changes the form and returns a checklist. The student tests keyboard navigation and screen-reader labels before accepting.",
    challenge: "What makes this guided rather than pure vibe coding?",
    choices: [
      {
        text: "The student asked for a trendy design.",
        feedback: "A trendy design does not verify accessibility.",
      },
      {
        text: "The student supplied constraints and manually checked the important interaction paths.",
        feedback:
          "Correct. Human direction and targeted checks are the bridge between casual prompting and full agentic engineering.",
      },
      {
        text: "The AI wrote all of the code without interruption.",
        feedback: "Hands-off generation alone does not make the work reliable.",
      },
    ],
    answer: 1,
  },
  {
    stage: "Agentic Engineering",
    badge: "Example 7",
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
  {
    stage: "Agentic Engineering",
    badge: "Example 8",
    learn:
      "Trajectory evaluation checks whether the agent followed the right path, not just whether the app appears to work.",
    scenario: "An agent updates a campus payment form for club dues.",
    aiMove:
      "Use the approved payment SDK only. Do not log card data. Run security tests and show the changed files before requesting review.",
    example:
      "The UI works, but the trace shows whether the agent touched forbidden files, added unsafe logging, or skipped the payment SDK.",
    challenge: "Which evidence matters most?",
    choices: [
      {
        text: "A screenshot of the successful payment button.",
        feedback: "A screenshot is useful, but it does not prove the agent avoided unsafe steps.",
      },
      {
        text: "Logs showing approved tools, no sensitive logging, and passing security checks.",
        feedback:
          "Correct. This evaluates the agent's trajectory and the final result.",
      },
      {
        text: "The agent saying it followed the rules.",
        feedback: "Claims are weaker than observable evidence from tools, logs, and tests.",
      },
    ],
    answer: 1,
  },
  {
    stage: "Agentic Engineering",
    badge: "Example 9",
    learn:
      "The factory model reduces long-term cost by routing work, loading context on demand, and matching model power to task difficulty.",
    scenario: "A capstone team wants agents to generate weekly test coverage reports.",
    aiMove:
      "Use a small model to summarize passing tests, a stronger model to analyze flaky failures, and CI gates to block unsafe changes.",
    example:
      "The harness routes simple summaries cheaply, sends hard debugging to a stronger model, and stores the evidence in the pull request.",
    challenge: "Which transcript concept does this demonstrate?",
    choices: [
      {
        text: "Intelligent model routing inside a mature harness.",
        feedback:
          "Correct. The system controls cost and quality by routing tasks instead of using the largest model for everything.",
      },
      {
        text: "Pure vibe coding because AI is involved.",
        feedback: "AI involvement alone does not define vibe coding. Verification and harness design define the mature workflow.",
      },
      {
        text: "Context rot because multiple models are used.",
        feedback: "Context rot is about overloaded irrelevant context, not model selection.",
      },
    ],
    answer: 0,
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
            <strong>${lesson.tag}</strong>
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
          <span>${beat.chapter}</span>
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
          Students can follow the full story step by step: why AI coding matters,
          how vibe coding works, why verification changes the game, how context and
          harness design mature the workflow, and why junior engineers still need judgment.
        </p>
      </div>
      <div class="journey-layout">
        <div class="beat-list" aria-label="Transcript learning beats">
          ${scriptBeatButtons()}
        </div>
        <article class="beat-detail" aria-live="polite">
          <div class="beat-detail__topline">
            <span id="beatChapter"></span>
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
          <span id="workshopProgress">0 of ${stageWorkshops.length} examples completed</span>
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
const beatChapter = document.querySelector("#beatChapter");
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

  beatChapter.textContent = beat.chapter;
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
