use crate::VaultError;
use std::time::{Duration, Instant};
#[derive(Clone, Copy, Debug, Default, PartialEq, Eq)]
pub enum Inactivity {
    OneMinute,
    #[default]
    FiveMinutes,
    FifteenMinutes,
    ThirtyMinutes,
}
impl Inactivity {
    pub fn from_minutes(minutes: u8) -> Result<Self, VaultError> {
        match minutes {
            1 => Ok(Self::OneMinute),
            5 => Ok(Self::FiveMinutes),
            15 => Ok(Self::FifteenMinutes),
            30 => Ok(Self::ThirtyMinutes),
            _ => Err(VaultError::InvalidPayload),
        }
    }
    pub fn duration(self) -> Duration {
        Duration::from_secs(match self {
            Self::OneMinute => 60,
            Self::FiveMinutes => 300,
            Self::FifteenMinutes => 900,
            Self::ThirtyMinutes => 1800,
        })
    }
}
#[derive(Clone, Copy)]
pub struct TimeoutToken {
    id: u64,
    generation: u64,
    deadline: Instant,
}
pub struct Session {
    id: u64,
    generation: u64,
    deadline: Instant,
    timeout: Inactivity,
}
impl Session {
    pub fn set_inactivity(&mut self, timeout: Inactivity, now: Instant) -> TimeoutToken {
        self.timeout = timeout;
        self.activity(now)
    }
    pub fn new(timeout: Inactivity, now: Instant) -> Self {
        static NEXT: std::sync::atomic::AtomicU64 = std::sync::atomic::AtomicU64::new(1);
        Self {
            id: NEXT.fetch_add(1, std::sync::atomic::Ordering::Relaxed),
            generation: 0,
            deadline: now + timeout.duration(),
            timeout,
        }
    }
    pub fn activity(&mut self, now: Instant) -> TimeoutToken {
        self.generation = self
            .generation
            .checked_add(1)
            .expect("session generation exhausted");
        self.deadline = now + self.timeout.duration();
        self.token()
    }
    pub fn token(&self) -> TimeoutToken {
        TimeoutToken {
            id: self.id,
            generation: self.generation,
            deadline: self.deadline,
        }
    }
    pub fn is_expired(&self, token: TimeoutToken, now: Instant) -> bool {
        token.id == self.id
            && token.generation == self.generation
            && token.deadline == self.deadline
            && now >= self.deadline
    }
}
