/**
 * Interview preparation — continuous track, CARL stories, and the 176-item roadmap.
 * Transcribed from README.md §Interview Preparation Integration and §Interview Preparation Roadmap.
 */

export interface CarlStory {
  story: string;
  weeks: string;
}

export const CARL_STORIES: CarlStory[] = [
  { story: 'Scope', weeks: '1–10' },
  { story: 'Ownership', weeks: '11–20' },
  { story: 'Ambiguity', weeks: '21–30' },
  { story: 'Perseverance', weeks: '31–40' },
  { story: 'Conflict resolution', weeks: '41–50' },
  { story: 'Growth', weeks: '51–60' },
  { story: 'Communication', weeks: '61–70' },
  { story: 'Leadership', weeks: '71–80' },
  { story: 'Technical trade-offs', weeks: '81–90' },
  { story: 'Production incident', weeks: '91–108' },
];

export const WEEKLY_MINIMUMS: string[] = [
  '1 coding drill',
  '1 system design question or pattern',
  '1 behavioral story refinement',
  '1 technical explanation out loud',
];

export interface InterviewFocus {
  weeks: string;
  focus: string;
}

export const INTERVIEW_FOCUS: InterviewFocus[] = [
  { weeks: '1–30', focus: 'Technical communication and basic problem solving' },
  { weeks: '31–45', focus: 'Coding patterns and implementation drills' },
  { weeks: '46–57', focus: 'System design case studies' },
  { weeks: '58–69', focus: 'ML/MLOps/experimentation interview questions' },
  { weeks: '70–81', focus: 'LLM/RAG/agent system design' },
  { weeks: '82–93', focus: 'LLM inference and performance questions' },
  { weeks: '94–102', focus: 'Production AI platform design' },
  { weeks: '103–108', focus: 'Full mock interviews' },
];

export interface RoadmapItem {
  step: string;
  item: string;
  type: string;
  completion: string;
}

export interface RoadmapTrack {
  name: string;
  count: number;
  items: RoadmapItem[];
}

export const ROADMAP_TRACKS: RoadmapTrack[] = [
  {
    name: 'System Design',
    count: 28,
    items: [
      { step: 'Reading', item: 'What is the system design interview?', type: 'Article', completion: 'Read' },
      { step: 'Reading', item: 'How to prepare for system design interviews', type: 'Article', completion: 'Read' },
      { step: 'Learning', item: 'Learn the delivery framework', type: 'Lesson', completion: 'Complete' },
      { step: 'Concepts', item: 'Study core system design concepts', type: 'Lesson', completion: 'Complete' },
      { step: 'Technologies', item: 'Learn key technologies', type: 'Lesson', completion: 'Complete' },
      { step: 'Problems', item: 'Top 10 Common Problems', type: 'Reading', completion: 'Read' },
      { step: 'Case Study', item: 'Design a URL Shortener', type: 'Design Exercise', completion: 'Complete' },
      { step: 'Case Study', item: 'Design Dropbox', type: 'Design Exercise', completion: 'Complete' },
      { step: 'Case Study', item: 'Design Ticketmaster', type: 'Design Exercise', completion: 'Complete' },
      { step: 'Case Study', item: 'Design FB News Feed', type: 'Design Exercise', completion: 'Complete' },
      { step: 'Case Study', item: 'Design WhatsApp', type: 'Design Exercise', completion: 'Complete' },
      { step: 'Case Study', item: 'Design LeetCode', type: 'Design Exercise', completion: 'Complete' },
      { step: 'Case Study', item: 'Design Uber', type: 'Design Exercise', completion: 'Complete' },
      { step: 'Case Study', item: 'Design a Web Crawler', type: 'Design Exercise', completion: 'Complete' },
      { step: 'Case Study', item: 'Design an Ad Click Aggregator', type: 'Design Exercise', completion: 'Complete' },
      { step: 'Case Study', item: 'Design Facebook’s Post Search', type: 'Design Exercise', completion: 'Complete' },
      { step: 'Pattern', item: 'Real-time Updates', type: 'Pattern', completion: 'Complete' },
      { step: 'Pattern', item: 'Dealing with Contention', type: 'Pattern', completion: 'Complete' },
      { step: 'Pattern', item: 'Multi-step Processes', type: 'Pattern', completion: 'Complete' },
      { step: 'Pattern', item: 'Scaling Reads', type: 'Pattern', completion: 'Complete' },
      { step: 'Pattern', item: 'Scaling Writes', type: 'Pattern', completion: 'Complete' },
      { step: 'Pattern', item: 'Handling Large Blobs', type: 'Pattern', completion: 'Complete' },
      { step: 'Pattern', item: 'Managing Long Running Tasks', type: 'Pattern', completion: 'Complete' },
      { step: 'Practice', item: 'Complete 3 easy guided practices', type: 'Milestone', completion: '3 Completed' },
      { step: 'Practice', item: 'Complete 3 medium guided practices', type: 'Milestone', completion: '3 Completed' },
      { step: 'Practice', item: 'Complete 2 hard guided practices', type: 'Milestone', completion: '2 Completed' },
      { step: 'Practice', item: 'Complete 3 easy guided practices (retry)', type: 'Milestone', completion: '3 Completed' },
    ],
  },
  {
    name: 'Coding',
    count: 20,
    items: [
      { step: 'Algorithm', item: 'Two Pointers', type: 'Topic', completion: 'Complete' },
      { step: 'Algorithm', item: 'Sliding Window', type: 'Topic', completion: 'Complete' },
      { step: 'Algorithm', item: 'Intervals', type: 'Topic', completion: 'Complete' },
      { step: 'Algorithm', item: 'Stack', type: 'Topic', completion: 'Complete' },
      { step: 'Algorithm', item: 'Linked List', type: 'Topic', completion: 'Complete' },
      { step: 'Algorithm', item: 'Binary Search', type: 'Topic', completion: 'Complete' },
      { step: 'Algorithm', item: 'Heap', type: 'Topic', completion: 'Complete' },
      { step: 'Algorithm', item: 'Depth-First Search', type: 'Topic', completion: 'Complete' },
      { step: 'Algorithm', item: 'Breadth-First Search', type: 'Topic', completion: 'Complete' },
      { step: 'Algorithm', item: 'Backtracking', type: 'Topic', completion: 'Complete' },
      { step: 'Algorithm', item: 'Graphs', type: 'Topic', completion: 'Complete' },
      { step: 'Algorithm', item: 'Dynamic Programming', type: 'Topic', completion: 'Complete' },
      { step: 'Algorithm', item: 'Greedy Algorithms', type: 'Topic', completion: 'Complete' },
      { step: 'Algorithm', item: 'Trie', type: 'Topic', completion: 'Complete' },
      { step: 'Algorithm', item: 'Prefix Sum', type: 'Topic', completion: 'Complete' },
      { step: 'Algorithm', item: 'Matrices', type: 'Topic', completion: 'Complete' },
      { step: 'Practice', item: 'Grind75', type: 'Question Set', completion: 'Complete' },
      { step: 'Practice', item: '50+ Company Tagged Questions', type: 'Question Set', completion: '50 Completed' },
      { step: 'Mock', item: 'Blank Editor + Think Aloud', type: 'Practice', completion: '5–7 Sessions' },
    ],
  },
  {
    name: 'Behavioral',
    count: 15,
    items: [
      { step: 'Reading', item: 'Why the behavioral interview matters', type: 'Article', completion: 'Read' },
      { step: 'Reading', item: 'Decode what questions are really asking', type: 'Article', completion: 'Read' },
      { step: 'Story', item: 'Scope', type: 'Story', completion: 'Prepared' },
      { step: 'Story', item: 'Ownership', type: 'Story', completion: 'Prepared' },
      { step: 'Story', item: 'Ambiguity', type: 'Story', completion: 'Prepared' },
      { step: 'Story', item: 'Perseverance', type: 'Story', completion: 'Prepared' },
      { step: 'Story', item: 'Conflict resolution', type: 'Story', completion: 'Prepared' },
      { step: 'Story', item: 'Growth', type: 'Story', completion: 'Prepared' },
      { step: 'Story', item: 'Communication', type: 'Story', completion: 'Prepared' },
      { step: 'Story', item: 'Leadership', type: 'Story', completion: 'Prepared' },
      { step: 'Story', item: 'Technical trade-offs', type: 'Story', completion: 'Prepared' },
      { step: 'Story', item: 'Production incident', type: 'Story', completion: 'Prepared' },
      { step: 'Mock', item: 'Mock interview #1', type: 'Mock Interview', completion: '1 Completed' },
      { step: 'Mock', item: 'Mock interview #2', type: 'Mock Interview', completion: '1 Completed' },
      { step: 'Mock', item: 'Mock interview #3', type: 'Mock Interview', completion: '1 Completed' },
    ],
  },
];

export const CAPSTONE_REQUIREMENTS: { area: string; requirement: string }[] = [
  { area: 'Product', requirement: 'Clear user problem, defined scope, working end-to-end flow' },
  { area: 'Architecture', requirement: 'API design, data model, retrieval/model flow, failure handling, tenant isolation' },
  { area: 'Evaluation', requirement: 'Offline metrics, online or simulated metrics, slice-based evaluation, error analysis' },
  { area: 'Observability', requirement: 'Logs, metrics, traces, dashboards, alert thresholds' },
  { area: 'Cost', requirement: 'Token usage, latency, cache hit rate, cost per request or per million tokens' },
  { area: 'Safety', requirement: 'Prompt injection defenses, PII redaction, guardrails, abuse prevention' },
  { area: 'Portfolio', requirement: 'Public repo, architecture diagram, benchmark report, demo video, design doc, interview summary' },
];

export const COMPLETION_LEVELS: { level: string; requires: string }[] = [
  { level: 'Foundations', requires: 'Core work shipped for Weeks 1–30, Gate 3 passed, Foundations portfolio release published' },
  { level: 'Engineering + Systems', requires: 'Core work shipped for Weeks 31–69, Gate 6 passed, Engineering + Systems release published' },
  { level: 'LLM Platform', requires: 'Core work shipped for Weeks 70–108, Gate 10 passed, final portfolio release published' },
  { level: 'Auror (optional)', requires: 'One program release plus all 548 Darbar entries solved and explained, required Forge spine, and both capstone boss artifacts attempted' },
];
