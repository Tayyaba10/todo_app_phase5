# # Multi-stage build for Next.js frontend
# FROM node:18-alpine AS deps
# RUN apk add --no-cache libc6-compat
# WORKDIR /src

# # Install dependencies
# COPY package.json yarn.lock* ./
# RUN npm install

# # Build the application
# FROM node:18-alpine AS builder
# WORKDIR /app
# COPY --from=deps /app/node_modules ./node_modules
# COPY . .

# # Build the Next.js app
# RUN yarn build

# # Production stage
# FROM node:18-alpine AS runner
# WORKDIR /app

# # Create non-root user for security
# RUN addgroup -g 1001 -S nodejs && \
#     adduser -S nextjs -u 1001

# # Copy built application
# COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
# COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static
# COPY --from=builder --chown=nextjs:nodejs /app/public ./public

# USER nextjs

# EXPOSE 3000

# ENV PORT=3000
# ENV NEXT_TELEMETRY_DISABLED=1

# CMD ["node", "server.js"]

FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .


ARG NEXT_PUBLIC_API_BASE_URL
ENV NEXT_PUBLIC_API_BASE_URL=$NEXT_PUBLIC_API_BASE_URL

RUN npm run build

EXPOSE 3000

CMD ["npm", "start"]
