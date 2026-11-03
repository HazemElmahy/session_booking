# Software Requirements Specification

## Session Booking with Reminders

---

## 1. Introduction

### 1.1 Purpose

This document captures every requirement in the product brief as a numbered, testable statement. It is the checklist for implementation, the reference for test coverage, and the list of open points that must be resolved and recorded in `DECISIONS.md`.

### 1.2 Scope

A small, working, end-to-end version of the ThoughtFull booking flow: a member finds a professional, sees their calendar, picks a date and time, and books a session. Both people receive reminders before the session starts.

### 1.3 Definitions

| Term | Meaning |
|---|---|
| Member | A person seeking support who books sessions. |
| Professional | A counsellor or coach who offers sessions. |
| Session | A meeting between exactly one member and one professional. Always 50 minutes long. |
| Availability | A professional's weekly working hours, set per day of the week, in the professional's timezone. |
| Slot | A candidate session start time generated from availability. |
| Reminder | A scheduled delivery of an in-app notification tied to a session. |
| Notification | An in-app message shown in a user's notification list. |

### 1.4 References

- ThoughtFull product brief: Session Booking with Reminders

---

## 2. Overall description

### 2.1 Users and roles

| Role | Description |
|---|---|
| Member | Books, views, cancels and reschedules their own sessions. |
| Professional | Sets availability, views their own schedule, cancels sessions. |

### 2.2 Domain rules

- DR-1. There are exactly two roles: member and professional.
- DR-2. Every user has a timezone, chosen at sign-up.
- DR-3. A session is always 50 minutes long.
- DR-4. A session is between one member and one professional.
- DR-5. Members and professionals are spread across several countries and timezones.

### 2.3 Constraints

- C-1. Any backend language, a modern web frontend and any database may be used.
- C-2. Fictional data only. No real personal data anywhere in the project.

### 2.4 Assumptions

- A-1. The server may restart at any time. No requirement may depend on in-memory state.
- A-2. Where the brief is silent, the implementer makes the choice, records it with reasoning in `DECISIONS.md`, and continues.

---

## 3. Functional requirements

Priority: all requirements in this section are **Must have**.

### FR-1. Sign up and login

- FR-1.1. A user can sign up as a member or as a professional.
- FR-1.2. At sign-up the user chooses a timezone.
- FR-1.3. A user can log in.
- FR-1.4. A user can log out.
- FR-1.5. On every request, the backend identifies the user from a token or session credential.
- FR-1.6. The backend never identifies the user from a user ID sent by the client.

### FR-2. Professional availability

- FR-2.1. A professional can set weekly working hours for each day of the week, for example Monday 09:00 to 17:00.
- FR-2.2. Working hours are expressed in the professional's own timezone.
- FR-2.3. Available slots are generated from the working hours.
- FR-2.4. The layout of slots within working hours is an implementation decision and must be explained in `DECISIONS.md`.

### FR-3. Find a professional

- FR-3.1. A member can see a list of professionals.
- FR-3.2. A member can open a professional's profile.

### FR-4. Calendar and booking

- FR-4.1. The professional's profile shows a calendar of available slots for the next 4 weeks.
- FR-4.2. Slots are shown in the member's timezone.
- FR-4.3. The member picks a date and time.
- FR-4.4. The member sees a confirmation screen before booking.
- FR-4.5. The member confirms and the session is booked.
- FR-4.6. A booked slot no longer appears as available.

### FR-5. No double-booking

- FR-5.1. A slot can be booked only once.
- FR-5.2. FR-5.1 holds even when two members try to book the same slot at the same moment.
- FR-5.3. A member cannot book two sessions that overlap in time.
- FR-5.4. FR-5.3 holds even when the two sessions are with different professionals.
- FR-5.5. Slots in the past cannot be booked.

### FR-6. My sessions

- FR-6.1. A member sees their upcoming sessions.
- FR-6.2. A member sees their past sessions.
- FR-6.3. A professional sees their own schedule of upcoming sessions.
- FR-6.4. The professional's schedule shows the member's name for each session.

### FR-7. Cancel and reschedule

- FR-7.1. A member can cancel a session up to 24 hours before it starts.
- FR-7.2. A member can reschedule a session up to 24 hours before it starts.
- FR-7.3. Within 24 hours of the start, both cancel and reschedule are blocked for the member.
- FR-7.4. When blocked, the member sees a clear message explaining why.
- FR-7.5. A professional can cancel a session at any time.
- FR-7.6. Rescheduling never leaves the member with no session.
- FR-7.7. Rescheduling never leaves the member with two sessions.

### FR-8. Reminders

- FR-8.1. When a session is booked, a reminder is scheduled for 24 hours before it starts.
- FR-8.2. When a session is booked, a reminder is scheduled for 1 hour before it starts.
- FR-8.3. Each reminder is scheduled for both the member and the professional.
- FR-8.4. Reminders are delivered as in-app notifications, shown in a notification list in the app.
- FR-8.5. A reminder whose delivery time has already passed at the moment of booking is not created.
- FR-8.6. Cancelling a session updates its reminders so that none are delivered for the cancelled session.
- FR-8.7. Rescheduling a session updates its reminders to match the new start time.
- FR-8.8. Each reminder is delivered exactly once.
- FR-8.9. FR-8.8 holds across a server restart.

### FR-9. Persistence

- FR-9.1. Users are stored in a database.
- FR-9.2. Availability is stored in a database.
- FR-9.3. Sessions are stored in a database.
- FR-9.4. Reminders are stored in a database.
- FR-9.5. All of the above survive a server restart.

### FR-10. Access control and privacy

- FR-10.1. Access control is enforced on the backend.
- FR-10.2. A member can see only their own sessions.
- FR-10.3. A member can change only their own sessions.
- FR-10.4. A professional can see only their own schedule.
- FR-10.5. A member viewing a professional's calendar sees only free slots.
- FR-10.6. A member viewing a professional's calendar never sees who else has booked.

---

## 4. Optional requirements

Priority: **Nice to have**. Attempt only once all of Section 3 works and is tested.

- OPT-1. A professional can block off specific dates, for example holidays.
- OPT-2. A minimum booking notice applies, for example no bookings less than 2 hours ahead.
- OPT-3. Everything runs with a single `docker compose up`.
- OPT-4. A deployed demo link is provided.

---

## 5. Out of scope

The following must not be built. If one of them matters, it is mentioned in `DECISIONS.md` instead.

- Password reset
- Email verification
- Social login
- Payments
- Video calls
- Recurring sessions
- Sync with external calendars such as Google or Outlook
- Real email, SMS or push delivery

---

## 6. Non-functional requirements

- NFR-1. **Time correctness.** All time handling is correct across timezones and daylight saving transitions.
- NFR-2. **Concurrency safety.** Double-booking prevention holds under concurrent requests, not only sequential ones.
- NFR-3. **Delivery reliability.** Reminder delivery is exactly once, independent of process lifetime.
- NFR-4. **Security.** Authentication and authorisation are enforced on the backend for every request. The client is never trusted for identity or role.
- NFR-5. **Durability.** No required behaviour depends on in-memory state.
- NFR-6. **Data.** Only fictional data is used, including seed and test data.

---

## 7. Testing requirements

- TR-1. Unit tests exist for the features built.
- TR-2. Tests prioritise the areas that matter most: slot generation, the 24-hour rule, timezones, double-booking, and reminder scheduling.
- TR-3. A high coverage number is not the goal.
- TR-4. All tests run with one documented command.

---

## 8. Deliverables

- D-1. A single GitHub repository containing backend, frontend and tests.
- D-2. A clear, incremental commit history.
- D-3. `README.md` containing:
  - prerequisites;
  - how to set up and run the app and the tests, ideally in one or two commands;
  - a short architecture overview, a simple diagram is welcome.
- D-4. `DECISIONS.md` containing:
  - key technical decisions and trade-offs;
  - assumptions made;
  - known limitations;
  - what would be done next with more time;
  - how double-booking is prevented;
  - how reminders are scheduled and delivered reliably;
  - how timezones and daylight saving changes are handled;
  - what would need to change to run this safely in production for a healthcare product.
- D-5. `AI_USAGE.md` containing:
  - which AI tools were used and for which parts;
  - at least one example where AI output was corrected, rejected or improved, with the reason.

---

## 9. Open points to resolve in DECISIONS.md

The brief deliberately leaves these unspecified. Each needs a decision and a recorded reason.

| ID | Open point | Related |
|---|---|---|
| OP-1 | How slots are laid out within working hours: grid interval, gap between sessions, alignment. | FR-2.4 |
| OP-2 | Exact meaning of "next 4 weeks": start boundary, end boundary, rolling from the current moment. | FR-4.1 |
| OP-3 | What happens to already-booked sessions when a professional changes availability. | FR-2.1, FR-6.3 |
| OP-4 | Whether cancelled sessions appear in "my sessions" and how they are marked. | FR-6.1, FR-6.2 |
| OP-5 | Whether a professional can reschedule. The brief grants cancel only. | FR-7.5 |
| OP-6 | Exact boundary behaviour of the 24-hour rule, at precisely 24 hours. | FR-7.1 to FR-7.3 |
| OP-7 | Content of a reminder notification, and whether a professional's reminder names the member. | FR-8.4 |
| OP-8 | How the professional is notified when a member cancels or reschedules, if at all. | FR-7 |
| OP-9 | Minimum validation rules for sign-up: email format, password length. | FR-1.1 |
| OP-10 | Source of the timezone list offered at sign-up. | FR-1.2 |
| OP-11 | What happens to existing sessions on a date the professional later blocks off. | OPT-1 |
| OP-12 | The value of the minimum booking notice. | OPT-2 |

